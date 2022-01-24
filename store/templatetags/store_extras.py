from django import template

from cart.models import CartItem

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def currency(amount):
    return f'${amount:.2f}'


@register.filter
def mult(arg1, arg2):
    return arg1 * arg2


@register.filter
def is_in_cart(product, cart):
    count = CartItem.objects.filter(
        cart__cart_id=cart.cart_id, product__id=product.id).count()
    if count:
        return True
    else:
        return False
