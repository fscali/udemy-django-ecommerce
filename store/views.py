from itertools import product
from django.shortcuts import render
from django.views.generic import View

from .models import Product

# Create your views here.


class StoreView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        return render(request, 'store/store.html', {
            'products': products,
            'products_count': products_count
        })
