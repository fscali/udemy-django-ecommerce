from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>',
         views.ActivateView.as_view(), name='activate'),
    path('recover_password/<uidb64>/<token>', views.PasswordRecoveryView.as_view(),
         name='password-recovery-link'),
    path('recover_password', views.PasswordRecoveryView.as_view(),
         name='password-recovery')
]
