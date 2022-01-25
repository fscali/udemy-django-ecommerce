from itertools import product
from math import ceil
from django.shortcuts import render
from django.views.generic import View

from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


from django.conf import settings

from .models import Product

from category.models import Category


# Create your views here.


class StoreView(View):
    def get(self, request, category_name='', product_slug=''):
        products = Product.objects.all().filter(is_available=True).order_by('id')

        selected_category = None
        selected_product = None
        cart = request.cart

        if product_slug:
            selected_product = Product.objects.get(
                slug=product_slug, category__slug=category_name)

        if category_name:
            selected_category = Category.objects.get(slug=category_name)
            products = products.filter(category=selected_category)
        search = request.GET.get('q')
        if search:
            products = products.filter(
                Q(product_name__icontains=search) | Q(description__icontains=search))
            q = f'&q={search}'
        else:
            q = ''

        products_count = products.count()
        page = request.GET.get('page', 1)  # self._get_page(request)
        paginator = Paginator(products, settings.RESULTS_PER_PAGE)
        paginated_products = paginator.get_page(page)
        if not selected_product:
            return render(request, 'store/store.html', {
                'products': paginated_products,
                'products_count': products_count,
                'selected_category': selected_category,
                'q': q
                #  'cart': cart,

            })
        else:
            return render(request, 'store/product.html', {
                'product': selected_product,
                'cart': cart
            })
