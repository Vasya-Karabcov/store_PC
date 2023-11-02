from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Category, Product


class HomeTemplateView(TemplateView):
    template_name = 'catalog/home_str.html'
    extra_context = {
        'title': 'Главная страница'
    }


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/product_list.html'
    extra_context = {
        'title': 'Каталог'
    }


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


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset - queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.object.get(self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk,
        context_data['title'] = f'Комплектующие {category_item.name}'

        return context_data
