
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin 
from rest_framework.generics import GenericAPIView

from .serializers import (  LoginSerializer,
                            PasswordSerializer,
                            UserSerializer , ForgetPasswordSerializer)

from rest_framework import viewsets
from django.contrib.auth.hashers import check_password
from rest_framework import status
from .models import ForgetPassword
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from base_rest.viewsets import BaseAPIViewSet

from django.contrib.auth import get_user_model
User = get_user_model()

from .mixins import AccountMixin


''' ModelViewSet for registering user '''

class AccountViewSet(BaseAPIViewSet , AccountMixin):
    queryset = User.objects.all()
    model_class = User
    serializer_class = UserSerializer
    instance_name = "user"
    ACTION_SERIALIZERS = {
        'reset': ForgetPasswordSerializer,
        'login': LoginSerializer,
    }
 
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'staus' : 200 , 'data' : serializer.data} ,status.HTTP_200_OK )



  
    
    
   
            
        
    




    