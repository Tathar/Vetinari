"""Veterini URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

from hosts import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'host', views.HostViewSet)
router.register(r'modbuswatcher', views.ModBusWatcherViewSet)
router.register(r'modbusresult', views.ModBusResultViewSet)

urlpatterns = [
    path('hosts/', include('hosts.urls')),
    path('admin/', admin.site.urls),
    path('api/v1.0/', include((router.urls))),
    path('api/v1.0/api-auth/', include('rest_framework.urls')),
]


from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
try :
    user = User.objects.get(is_superuser=True)
except ObjectDoesNotExist:
    user = User.objects.create_superuser('admin', '', 'admin')

