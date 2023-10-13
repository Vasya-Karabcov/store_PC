from django.shortcuts import render


def index(request):
    return render(request, 'catalog/home_str.html')


def index_con(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f' {name}, {phone}\n {message}')
    return render(request, 'catalog/contact.html')
