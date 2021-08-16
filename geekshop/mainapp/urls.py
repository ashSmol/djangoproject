from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import products, product, products_ajax

app_name = 'products'
urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('category/<int:pk>/ajax/', cache_page(3600)(products_ajax)),
    path('product/<int:pk>/', product, name='product'),
    path('category/<int:pk>/page/<int:page>/', products, name='page'),
    path('category/<int:pk>/page/<int:page>/ajax/', cache_page(3600)(products_ajax)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
