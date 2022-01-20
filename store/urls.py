
from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='store'),
    path('categories/<slug:category_name>',
         views.StoreView.as_view(), name='store-categories')
    #path('', views.home, name="home")
]
