from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
 
    path('register/' , RegisterView),
    path('login/' , Login),
    path('forget-password/' , ForgetPassword),
    
    path('verify/<token>/' , verify_email),
    path('change-password/<token>/' , change_password),
    
]
