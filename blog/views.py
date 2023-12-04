from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Добавить новую запись:'
    }

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.owner = self.request.user
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'body',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    # def get_object(self, queryset=None):
    #     title = super().get_object(queryset)
    #     blog = get_object_or_404(Blog, title=title)
    #     user_groups = [group.name for group in self.request.user.groups.all()]
    #     if blog.owner != self.request.user and 'Managers' not in user_groups:
    #         raise Http404
    #     return blog

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get("pk")])


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_group_names = [group.name for group in user.groups.all()]
        context['user_group_names'] = user_group_names
        return context


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def get_object(self, queryset=None):
        title = super().get_object(queryset)
        blog = get_object_or_404(Blog, title=title)
        user_groups = [group.name for group in self.request.user.groups.all()]
        if blog.owner != self.request.user and 'Managers' not in user_groups:
            raise Http404
        return blog
