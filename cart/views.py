from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class CartView(View):
    def get(self, request):
        return render(request, 'store/cart.html')
