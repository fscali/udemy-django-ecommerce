from django.db import models
from functools import reduce
from operator import add

import logging

from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def total(self):
        result = reduce(add, (item.product.price *
                        item.quantity for item in self.cart_items.all()), 0)
        return result

    def tax(self):
        return (2*self.total()) / 100

    def grand_total(self):
        return self.total() + self.tax()


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, related_name='cart_items')

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name

    def total(self):
        return self.product.price * self.quantity

    def color(self):
        return self.variations.get(variation_category='color').variation_value

    def size(self):
        return self.variations.get(variation_category='size').variation_value
