
from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreView.as_view()),
    #path('', views.home, name="home")
]
