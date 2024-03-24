from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('main.urls',namespace='main')),
    path('accounts', include('django.contrib.auth.urls')),
]
