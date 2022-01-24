
from .models import Cart


def cart_count(request):

    cart = request.cart
    count = cart.cart_items.count()

    return dict(cart_count=count)
