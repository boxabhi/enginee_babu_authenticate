from django.contrib import admin
from django.urls import path, include
from .views import (AccountViewSet , Login , ResetPasswordRequestToken,verify_email,ResetPasswordRequest)
from rest_framework import routers
router = routers.DefaultRouter()
router.register('register' ,AccountViewSet )
urlpatterns = [
    path('' , include(router.urls)),    
    path('login/' , Login.as_view()),
    path('forget-password/' , ResetPasswordRequestToken.as_view()),
    path('verify/<token>/' , verify_email),
    path('change-password/<token>/' , ResetPasswordRequest.as_view()),
]
