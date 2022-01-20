from itertools import product
from unicodedata import category
from django.shortcuts import render
from django.views.generic import View

from .models import Product

from category.models import Category


# Create your views here.


class StoreView(View):
  # Story.objects.get(slug=self.kwargs['slug'])
    def get(self, request, category_name=''):
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
        selected_category = None

        #category_name = self.kwargs.get('category_name')

        if category_name:
            selected_category = Category.objects.get(slug=category_name)
            products = products.filter(category=selected_category)

        categories = Category.objects.all()
        return render(request, 'store/store.html', {
            'products': products,
            'products_count': products_count,
            'categories': categories,
            'selected_category': selected_category
        })
