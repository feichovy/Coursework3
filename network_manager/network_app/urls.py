from django.urls import path
from . import views

urlpatterns = [
    path('config_device/', views.config_device, name='config_device'),
]
