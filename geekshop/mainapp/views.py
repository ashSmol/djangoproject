from django.shortcuts import render
from .models import Product, ProductCategory


def products(request):
    title = 'продукты\товары'
    products_list = Product.objects.all()[:4]

    links_menu = ProductCategory.objects.all()

    context = {
        'title': title,
        'links_menu': links_menu,
        'products_list': products_list,
    }
    return render(request, 'mainapp/products.html', context=context)
