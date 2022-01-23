
from django.shortcuts import render
from django.views.generic import View

from store.models import Product
from .models import Cart, CartItem

# Create your views here.


class CartView(View):
    def get(self, request):
        cart_id = self._cart_id(request)
        cart = Cart.objects.get(cart_id=cart_id)
        ctx = self._get_ctx(cart)
        return render(request, 'store/cart.html', ctx)

    def post(self, request):
        cart_item_id = request.POST.get('cart_item')
        if cart_item_id:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart = cart_item.cart
            cart_item.delete()

            pass
        else:
            product_id = request.POST.get('product_id')
            sign = request.POST.get('sign')
            sign = int(sign) if sign else 1
            if product_id:
                product = Product.objects.get(id=product_id)
                try:
                    cart = Cart.objects.get(cart_id=self._cart_id(request))
                except Cart.DoesNotExist:
                    cart = Cart.objects.create(
                        cart_id=self._cart_id(request)
                    )
                try:
                    cart_item = CartItem.objects.get(
                        product=product, cart=cart)
                    cart_item.quantity += sign
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        product=product, cart=cart, quantity=1)
                    cart_item.save()
        ctx = self._get_ctx(cart)
        return render(request, 'store/cart.html', ctx)

    def _cart_id(self, request):
        cart = request.session.session_key
        if not cart:
            cart = request.session.create()
        return cart

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
