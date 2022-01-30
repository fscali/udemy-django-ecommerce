from django.urls import path, include
from . import views

urlpatterns = [
    path('place_order', views.PlaceOrderView.as_view(), name='place-order'),
    path('payments', views.PaymentsView.as_view(), name='payments')
]
