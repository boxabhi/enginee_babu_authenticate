
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
from .models import *

from .serializers import (  LoginSerializer,
                            PasswordSerializer,
                            UserSerializer ,ChangePasswordSerializer, ForgetPasswordSerializer)
from django.contrib.auth import get_user_model


class AccountMixin:
    
    @action(detail=False, methods=['post'] ,url_path="login" ,url_name="login"  )
    def login(self , request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.login()
    
    
    @action(detail=False, methods=['post'] , url_path="reset" ,url_name="reset")
    def reset(self , request):
        serializer = ForgetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.forget_password()
        response =   {'status': 200 , 'message': 'An email is sent to you' }
        return Response(response , status.HTTP_200_OK)
    
    
    @action(detail=False , methods=['put'] , url_path="change-password" ,url_name="change-password")
    def change_password(self,request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.change_password() 
        response = {'staus' : 200 , 'message' : 'Password changed'}
        return Response(response , status.HTTP_200_OK)