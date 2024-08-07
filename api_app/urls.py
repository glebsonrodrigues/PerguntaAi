# api_app/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # URL para a página principal
    path('login/', auth_views.LoginView.as_view(template_name='api_app/login.html'), name='login'),  # URL para a página de login
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # URL para o logout
]
