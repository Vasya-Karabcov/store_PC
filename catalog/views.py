from django.shortcuts import render

from catalog.models import Category, Product


def index(request):
    category_list = Category.objects.all()
    context = {
        'object_list': category_list,
        'title': 'Главная'
    }
    return render(request, 'catalog/home_str.html', context)


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


def index_product(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Процессоры',
    }
    return render(request, 'catalog/product.html', context)
