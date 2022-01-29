
from functools import reduce
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from store.models import Product, Variation
from .models import Cart, CartItem

# Create your views here.


class CartView(View):
    def get(self, request):
        cart = request.cart
        ctx = self._get_ctx(cart)
        return render(request, 'store/cart.html', ctx)

    def post(self, request):
        cart_item_id = request.POST.get('cart_item')
        if cart_item_id:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart = cart_item.cart
            cart_item.delete()
        else:
            product_id = request.POST.get('product_id')
            if product_id:
                sign = int(request.POST['sign']
                           ) if 'sign' in request.POST else 1

                # {'color', 'size'}
                variation_categories = {v["variation_category"] for v in Variation.objects.filter(
                    product__id=product_id).values('variation_category').distinct()}

                # {'color': 'red', 'size': 'small'}
                variation_fields = {
                    k: request.POST[k] for k in variation_categories.intersection(request.POST.keys())}

                # [Q(variation_category='color') & Q(variation_value='red'), Q(variation_category='size') & Q(variation_value='small')]
                variation_queries = map(lambda x: Q(variation_category=x[0]) & Q(
                    variation_value=x[1]), variation_fields.items())

                variation_queries = reduce(
                    lambda a, b: a | b, variation_queries, Q())

                product = Product.objects.get(id=product_id)

                variations = Variation.objects.filter(
                    Q(product=product), variation_queries)

                cart = request.cart
                try:
                    cart_item = CartItem.objects.filter(
                        product=product, cart=cart)
                    for v in variations:
                        cart_item = cart_item.filter(variations__id=v.id)

                    cart_item = cart_item.get()
                    cart_item.quantity += sign
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        product=product, cart=cart, quantity=1)
                    for v in variations:
                        cart_item.variations.add(v)
                    cart_item.save()
        ctx = self._get_ctx(cart)
        return render(request, 'store/cart.html', ctx)

    def _cart_id(self, request):
        """ cart = request.session.session_key
        if not cart:
            request.session.create()
            cart = request.session.session_key
        return cart """
        return request.cart_id

    def _get_ctx(self, cart):
        ctx = {}
        if cart:
            cart_items = cart.cart_items.all()
            ctx['cart_items'] = cart_items
            ctx['total'] = cart.total()
            ctx['tax'] = cart.tax()
            ctx['grand_total'] = cart.grand_total()
        else:
            ctx['cart_items'] = []
            ctx['total'] = 0
            ctx['tax'] = 0
            ctx['grand_total'] = 0
        return ctx


class CheckoutView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return render(request, 'store/checkout.html')
