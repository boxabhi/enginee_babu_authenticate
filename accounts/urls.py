from django.contrib import admin
from django.urls import path, include
from .views import (AccountViewSet , ResetPasswordRequestToken,verify_email,ResetPasswordRequest)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'auth' ,AccountViewSet )


urlpatterns = [
    path('' , include(router.urls)),    
    path('forget-password/' , ResetPasswordRequestToken.as_view()),
    path('verify/<token>/' , verify_email),
    path('change-password/<token>/' , ResetPasswordRequest.as_view()),
]
