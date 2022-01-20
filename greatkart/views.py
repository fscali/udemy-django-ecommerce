from django.shortcuts import render
from django.views.generic.list import ListView

from store.models import Product


class HomeView(ListView):
    queryset = Product.objects.filter(is_available=True)
    model = Product
    context_object_name = 'products'
    template_name = 'home.html'


""" def home(request):
    return render(request, 'home.html')
 """
