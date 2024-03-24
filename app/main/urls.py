from django.urls import path

from main import views
from main.views import profile_view

app_name = 'main'

urlpatterns = [
    # path('', views.index, name='profile'),
    path('', profile_view, name='profile'),
    # path('profile/', profile_view, name='profile'),
]
