from django.shortcuts import render
from django.views.generic import ListView

from mainapp.models import Product, ProductCategory

class ProductsListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'objects'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['title'] = 'Магазин'

        return context

    def get_queryset(self):
        return Product.objects.all().order_by('-is_active')

# def index(request):
#     title = 'магазин'
#     products_list = Product.objects.all()
#     context = {
#         'title':title,
#         'products_list':products_list,
#     }
#     return render(request, 'index.html', context=context)

def contacts(request):
    title = 'контакты'
    context = {
        'title':title
    }
    return render(request, 'contact.html', context=context)