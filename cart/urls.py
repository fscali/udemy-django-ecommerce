from django.urls import path
from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout')
]
