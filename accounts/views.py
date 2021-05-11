
from django.contrib import auth
from django.shortcuts import render, redirect
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from rest_framework.authtoken.models import Token
import uuid
from .helpers import *
from .serializers import *

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin , UpdateModelMixin

from rest_framework.generics import GenericAPIView



from rest_framework_simplejwt.views import TokenObtainPairView

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(generics.GenericAPIView , CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email' 
    def post(self,request , *args, **kwargs):
        return self.create(request,*args ,**kwargs)
    
RegisterView = RegisterView.as_view()



class ResetPasswordRequestToken(GenericAPIView):
    serializer_class = EmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_obj = User.objects.filter(email=email).first()
        
        response = {'status': 500 , 'message' : 'Something went wrong'}
        if user_obj is None:
            response['message'] = 'no user found with username'
            raise Exception('no user found with username  is required')
        send_reset_password_email(user_obj)            
        response['status'] = 200
        response['message'] = 'An email is sent to you'
        
        return Response(response)
        
Forget = ResetPasswordRequestToken.as_view() 
    

from django.contrib.auth.hashers import check_password

class Login(APIView):

    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            
            email = data.get('email')
            password = data.get('password')

            if User.objects.filter(email = email).first() is None:
                response['message'] = 'user not found'
                return Response(response)

            

            user_obj = User.objects.get(email = email)       
            password_check = check_password(password ,user_obj.password )

            print(user_obj)
            if user_obj is None:
                response['message'] = 'invalid credentials'
                return Response(response)

            refresh = RefreshToken.for_user(user_obj)
            response['refresh'] = str(refresh)
            response['access'] =  str(refresh.access_token)
            response['status'] = 200
            response['message'] = 'Login Success'

            return Response(response)
              


        except Exception as e:
            print(e)


Login  = Login.as_view()
class ResetPasswordRequest(GenericAPIView):
    serializer_class = PasswordSerializer
    
    def put(self, request,token ,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        response = {'status': 500 , 'message' : 'Something went wrong'}
        user_obj = None
        try:
            user_obj = User.objects.get(forget_password_token=token)
        except Exception as e: 
            response['message'] = 'Invalid Token'
            return Response(response)
        
        user_obj.forget_password_token= None
        user_obj.set_password(password)
        user_obj.save()
        response['status'] = 200
        response['message'] = 'Password Changed'
        return Response(response)
            

ResetPasswordRequest  = ResetPasswordRequest.as_view()      

    



def verify_email(request , token):
    try:
        user_obj = User.objects.get(email_verification_token=  token)
        user_obj.is_verified = True
        user_obj.save()
        
    except Exception as e: 
        print(e)
        return JsonResponse({'status' : 500 , 'message' : 'Something went wrong'})
       
    return render(request, 'account_verified.html')
    




    

