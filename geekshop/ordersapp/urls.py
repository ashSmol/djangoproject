from django.urls import path

from .views import OrderList, OrderItemsCreate, OrderItemsUpdate, OrderRead, OrderDelete, order_forming_complete

app_name = 'ordersapp'
urlpatterns = [
    path('', OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', order_forming_complete, name='order_forming_complete'),
    path('create/', OrderItemsCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', OrderDelete.as_view(), name='order_delete'),
]
