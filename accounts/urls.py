from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
 
    path('register/' , RegisterView),
    path('forget-password/' , Forget),

    path('verify/<token>/' , verify_email),
    path('change-password/<token>/' , ResetPasswordRequest),
    
]
