from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_map = {
        'name': 'name',
        'min_price': 'price',
        'max_price': '-price',
    }
    sort = request.GET.get('sort')

    if sort:
        phones_objects = Phone.objects.all().order_by(sort_map[sort])
    else:
        phones_objects = Phone.objects.all()

    context = {
        'phones': phones_objects,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone_objects = Phone.objects.filter(slug=slug)
    phone = [phone for phone in phone_objects]
    context = {
        'phone': phone_objects[0]

    }
    return render(request, template, context)
