from random import sample

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView

from blog.models import Blog
from catalog.forms import ProductForm, VersionForm, MailingForm, ClientForm, MessageForm
from catalog.models import Category, Product, Version, Mailing, Client, Message, Log
from catalog.services import get_category_cache
from config.settings import CACHE_ENABLED


class HomeTemplateView(TemplateView):
    template_name = 'catalog/home_str.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_mailing'] = len(Mailing.objects.all())
        active_mailings_count = Mailing.objects.filter(status__in=['created', 'started']).count()
        context['active_mailings_count'] = active_mailings_count
        unique_clients_count = Client.objects.filter(is_active=True).distinct().count()
        context['unique_clients_count'] = unique_clients_count
        all_posts = list(Blog.objects.all())
        context['random_blog_posts'] = sample(all_posts, min(3, len(all_posts)))
        context['object_list'] = Mailing.objects.all()
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class MailingListView(ListView):
    model = Mailing
    template_name = 'catalog/mailing_list.html'
    context_object_name = 'mailings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'catalog/create_mailing.html'

    def form_valid(self, form):
        new_mailing = form.save()
        new_mailing.owner = self.request.user
        new_mailing.save()
        self.mailing_pk = new_mailing.pk
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('catalog:create_message', kwargs={'mailing_pk': self.mailing_pk})


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    fields = ('start_time', 'frequency', 'recipients', 'status')
    success_url = reverse_lazy('catalog:mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.owner = self.request.user
            new_mailing.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        mailing = get_object_or_404(Mailing, id=mailing.pk)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if mailing.owner != self.request.user and 'Managers' not in user_groups:
            raise Http404
        return mailing


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'catalog/mailing_detail.html'
    context_object_name = 'mailing'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = Message.objects.filter(mailing=self.object)
        return context


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('catalog:mailing')
    extra_context = {
        'title': 'Удаление записи:'
    }

    def get_object(self, queryset=None):
        mailing = super().get_object(queryset)
        mailing = get_object_or_404(Mailing, id=mailing.pk)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if mailing.owner != self.request.user and 'Managers' not in user_groups:
            raise Http404
        return mailing


class ClientListView(ListView):
    model = Client
    template_name = 'catalog/client_list.html'
    context_object_name = 'clients'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('catalog:catalog')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=None, **kwargs)
        data['title'] = "Создание нового клиента."
        return data

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('catalog:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('catalog:client_list')


class MessageListView(ListView):
    model = Message  # Corrected from Client to Message
    template_name = 'catalog/message_list.html'
    context_object_name = 'messages'  # Corrected from 'message' to 'messages'

    def get_queryset(self):
        mailing_pk = self.kwargs['mailing_pk']
        return Message.objects.filter(mailing__pk=mailing_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        context['mailing_pk'] = self.kwargs['mailing_pk']
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'catalog/create_message.html'
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['mailing_pk'])
        message = form.save(commit=False)
        message.mailing = mailing
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('catalog:catalog')

    def form_valid(self, form):
        mailing = get_object_or_404(Mailing, pk=self.kwargs['mailing_pk'])
        message = form.save(commit=False)
        message.mailing = mailing
        message.save()
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('catalog:catalog')


class DeliveryReportView(ListView):
    model = Log
    template_name = 'catalog/delivery_report.html'
    context_object_name = 'delivery_logs'

    def get_queryset(self):
        return Log.objects.filter(status='success')


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    extra_context = {
        'title': 'Каталог'
    }

    def get_queryset(self):
        return get_category_cache()


@login_required
def index_con(request):
    context = {
        'title': 'Контакты',
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f' {name}, {phone}\n {message}')
    return render(request, 'catalog/contact.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'), get_user=self.request.user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'Комплектующие {category_item.name}'

        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.get_user = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:category_list')
    permission_required = 'catalog.change_product'

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #     if self.object.get_user != self.request.user:
    #         raise f'Нет доступа'
    #     return self.object

    def get_success_url(self):
        return reverse('catalog:edit_product', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        contex_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        contex_data['formset'] = formset
        return contex_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:category_list')
