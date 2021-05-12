from django.contrib import admin
from django.urls import path, include
from .views import AccountViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('auth' ,AccountViewSet )


urlpatterns = [
    path('' , include(router.urls)),    
   
]
