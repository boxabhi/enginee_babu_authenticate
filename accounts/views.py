
import uuid
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin 
from rest_framework.generics import GenericAPIView

from .serializers import (  EmailSerializer,
                            PasswordSerializer,
                            UserSerializer , ForgetPasswordSerializer)
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework import viewsets
from django.contrib.auth.hashers import check_password
from rest_framework import status
from .models import ForgetPassword
User = get_user_model()


''' ModelViewSet for registering user '''

class AccountViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
 


class ResetPasswordRequestToken(GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_obj = User.objects.filter(email=email).first()
        
        response = {'status': 500 , 'message' : 'Something went wrong'}
        if user_obj is None:
            response['message'] = 'no user found with username'
            raise Exception('no user found with username  is required')
        
        token = str(uuid.uuid4())
        ForgetPassword.objects.create(user = user_obj ,forget_password_token = token )
                   
        response['status'] = 200
        response['message'] = 'An email is sent to you'
        
        return Response(response)
         
    


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
                return Response(response , status.HTTP_403_FORBIDDEN)

            user_obj = User.objects.get(email = email)         
            if not check_password(password ,user_obj.password):
                response['message'] = 'invalid credentials'
                return Response(response)
            
            refresh = RefreshToken.for_user(user_obj)
            refresh = {''}
            response = {'refresh' : str(refresh) ,'access' :str(refresh.access_token), 'message' : 'Login Success'}
            return Response(response , status.HTTP_200_OK)
              
        except Exception as e:
            print(e)
        return Response(response , status.HTTP_400_BAD_REQUEST)



class ResetPasswordRequest(GenericAPIView):
    serializer_class = PasswordSerializer
    
    def put(self, request,token ,  *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        response = {'status': 500 , 'message' : 'Something went wrong'}
        forget_password_obj = None
        try:
            forget_password_obj = ForgetPassword.objects.get(forget_password_token=token)
        except Exception as e: 
            response['message'] = 'Invalid Token'
            return Response(response  ,  status.HTTP_404_NOT_FOUND)
        
        user_obj = User.objects.get(id = forget_password_obj.user.id)

        user_obj.forget_password_token= None
        user_obj.set_password(password)
        user_obj.save()
    
        response = {'staus' : 200 , 'message' : 'Password changed'}
        return Response(response , status.HTTP_200_OK)
            





def verify_email(request , token):
    try:
        user_obj = User.objects.get(email_verification_token=  token)
        user_obj.is_verified = True
        user_obj.save()
    except Exception as e: 
        print(e)
        return JsonResponse({'status' : 500 , 'message' : 'Something went wrong'})
    return render(request, 'account_verified.html')
    


class RegisterView(generics.GenericAPIView , CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email' 
    def post(self,request , *args, **kwargs):
        return self.create(request,*args ,**kwargs)
    