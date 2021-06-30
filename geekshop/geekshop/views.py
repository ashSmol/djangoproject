from django.shortcuts import render
from mainapp.models import Product, ProductCategory
def index(request):
    title = 'магазин'
    products_list = Product.objects.all()
    context = {
        'title':title,
        'products_list':products_list,
    }
    return render(request, 'index.html', context=context)

def contacts(request):
    title = 'контакты'
    context = {
        'title':title
    }
    return render(request, 'contact.html', context=context)