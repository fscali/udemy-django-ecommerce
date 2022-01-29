from django.db import models
from django.db.models.query import Q
from functools import reduce
from operator import add

from functools import reduce

from accounts.models import Account
from store.models import Product, Variation

# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name='carts')

    def __str__(self):
        return self.cart_id

    def __bool__(self):
        return self.cart_items.all().exists()

    @staticmethod
    def from_request(request):
        cart_id = request.session.session_key
        if not cart_id:
            request.session.create()
            cart_id = request.session.session_key

        request.cart_id = cart_id

        try:
            cart = Cart.objects.get(cart_id=request.cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=request.cart_id)
        return cart

    def total(self):
        result = reduce(add, (item.product.price *
                        item.quantity for item in self.cart_items.all()), 0)
        return result

    def tax(self):
        return (2*self.total()) / 100

    def grand_total(self):
        return self.total() + self.tax()

    def transfer_from(self, cart_from):
        if cart_from:
            for item in cart_from.cart_items.all():
                filters = map(lambda v: Q(
                    variations__variation_category=v.variation_category, variations__variation_value=v.variation_value), item.variations.all())

                my_item = self.cart_items.filter(
                    product=item.product)

                for f in filters:
                    my_item = my_item.filter(f)
                if my_item.exists():
                    found = my_item[0]
                    found.quantity += item.quantity
                    found.save()

                else:
                    self.cart_items.add(item)


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
