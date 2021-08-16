from django.db import models

from geekshop.settings import AUTH_USER_MODEL
from mainapp.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,

    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )
    add_datetime = models.DateTimeField(
        verbose_name='время добавления',
        auto_now_add=True
    )

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()


    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return total_quantity

    @property
    def total_cost(self):
        _items = self.get_items_cached
        total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()
