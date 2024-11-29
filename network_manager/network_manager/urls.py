"""
URL configuration for network_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='home'),  # 根路径对应 Welcome 主页面
    path('welcome/', views.welcome, name='welcome'),  # 添加一个路径 'welcome/'，也能访问 Welcome 页面
    path('config_device/', views.config_device, name='config_device'),
    path('config_ospf/', views.config_ospf, name='config_ospf'),
    path('config_ipsec/', views.config_ipsec, name='config_ipsec'),
    path('config_acl/', views.config_acl, name='config_acl'),
]