
from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('categories/<slug:category_name>',
         views.StoreView.as_view(), name='store-categories'),
    path('categories/<slug:category_name>/<slug:product_slug>', views.StoreView.as_view(), name='product-detail'
         )
    #path('', views.home, name="home")
]
