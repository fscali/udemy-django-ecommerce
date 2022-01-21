from itertools import product
from unicodedata import category
from django.shortcuts import render
from django.views.generic import View

from .models import Product

from category.models import Category


# Create your views here.


class StoreView(View):
    def get(self, request, category_name=''):
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        selected_category = None

        if category_name:
            selected_category = Category.objects.get(slug=category_name)
            products = products.filter(category=selected_category)

        return render(request, 'store/store.html', {
            'products': products,
            'products_count': products_count,
            'selected_category': selected_category
        })
