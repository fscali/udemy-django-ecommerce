from itertools import product
from math import prod
from unicodedata import category
from django.shortcuts import render
from django.views.generic import View

from .models import Product

from category.models import Category


# Create your views here.


class StoreView(View):
    def get(self, request, category_name='', product_slug=''):
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        selected_category = None
        selected_product = None

        if product_slug:
            selected_product = Product.objects.get(
                slug=product_slug, category__slug=category_name)

        if category_name:
            selected_category = Category.objects.get(slug=category_name)
            products = products.filter(category=selected_category)

        if not selected_product:
            return render(request, 'store/store.html', {
                'products': products,
                'products_count': products_count,
                'selected_category': selected_category
            })
        else:
            return render(request, 'store/product.html', {
                'product': selected_product
            })
