from .models import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        cart_id = request.session.session_key
        if not cart_id:
            request.session.create()
            cart_id = request.session.session_key

        request.cart_id = cart_id

        try:
            cart = Cart.objects.get(cart_id=request.cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=request.cart_id)
        request.cart = cart

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
