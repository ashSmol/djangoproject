from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from basketapp.views import basket_add, basket_remove, basket

app_name = 'basketapp'
urlpatterns = [
    path('', basket, name='view'),
    path('add/<int:pk>/', basket_add, name='add'),
    path('remove/<int:pk>)/', basket_remove, name='remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
