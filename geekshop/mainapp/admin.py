from django.contrib import admin

from authapp.models import ShopUser
from .models import ProductCategory, Product

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ShopUser)
