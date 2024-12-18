from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='home'),  # 根路径指向 welcome 视图
    path('config_device/', views.config_device, name='config_device'),
    path('config_ospf/', views.config_ospf, name='config_ospf'),
    path('config_ipsec/', views.config_ipsec, name='config_ipsec'),
    path('config_acl/', views.config_acl, name='config_acl'),
]
