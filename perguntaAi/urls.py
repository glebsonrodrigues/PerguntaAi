from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api_app.urls')),  # Inclui as URLs do aplicativo api_app
]
