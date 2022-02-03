from .models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cart = self._get_cart_from_user(request)
        if not cart:
            cart = Cart.from_request(request)

        request.cart = cart

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def _get_cart_from_user(self, request):
        if not request.user.is_anonymous:
            cart = request.user.carts.exclude(status='completed').exclude(
                status='canceled').order_by('-date_added').first()

            return cart
        return None
