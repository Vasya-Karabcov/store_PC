from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Version
from catalog.services import get_category_cache
from config.settings import CACHE_ENABLED


class HomeTemplateView(TemplateView):
    template_name = 'catalog/home_str.html'
    extra_context = {
        'title': 'Главная страница'
    }


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
