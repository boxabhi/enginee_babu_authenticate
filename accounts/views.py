
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from rest_framework.authtoken.models import Token
import uuid
from .helpers import *

from django.http import JsonResponse



class RegisterView(APIView):
    
    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        
        try:
            data = request.data
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            username = data.get('username')
            password = data.get('password')
            
            ''' CHECKING REQUEST PACKET KEY IS PRESENT OR NOT '''
            
            if first_name is None:
                response['message'] = 'first name is required'       
                raise Exception('first name is required')

            if last_name is None:
                response['message'] = 'last name is required'       
                raise Exception('first name is required')
                
            if email is None:
                response['message'] = 'email is required'       
                raise Exception('first name is required')

            if username is None:
                response['message'] = 'username is required'
                raise Exception('username  is required')
                
            ''' VALIDATING IF USERNAME OR EMAIL ALREADY EXISTS '''
            
            if User.objects.filter(username = username).first():
                response['message'] = 'username is taken'
                raise Exception('username  is required')
        
            if User.objects.filter(email = email).first():
                response['message'] = 'email is taken'
                raise Exception('email  is required')
            
            ''' CREATING USER '''
            user_obj = User.objects.create(username = username, email = email , first_name =first_name , last_name =last_name)    
            user_obj.set_password(password)
            user_obj.save()
            
            response['status'] = 200
            response['message'] = 'Your account has been created check your email'
             
        except Exception as e:
            print(e)
        
        return Response(response)
            
RegisterView = RegisterView.as_view()


class Login(APIView):
    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        
        try:
            data = request.data
            username = data.get('username')
            password = data.get('password')
            
            if username is None:
                response['message'] = 'username is required'
                raise Exception('username  is required')
        
            if password is None:
                response['message'] = 'password is required'
                raise Exception('password  is required')
            
            
            if User.objects.filter(username=username).first() is None:
                response['message'] = 'no user found with username'
                raise Exception('no user found with username  is required')
                
            
            user_obj = authenticate(username=username, password=password)
            
            if user_obj is None:
                response['message'] = 'Invalid Password'
                raise Exception('invalid password')
            
            if user_obj.is_verified is False:
                response['message'] = 'Your account is not verified'
                raise Exception('account not verified')
                

            
            token = Token.objects.get_or_create(user=user_obj)
            print(token[0])
            
            response['message'] = 'login successful'
            response['status'] = 200
            response['token'] = str(token[0])
            
        except Exception as e:
            print(e)
            
        return Response(response)
            

Login = Login.as_view()

class ForgetPassword(APIView):
    def post(self , request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong'
        try:
            data = request.data
            username = data.get('username')
            
            if username is None:
                response['message'] = 'username is required'
                raise Exception('username  is required')
            
            user_obj = User.objects.filter(username=username).first()
            
            if user_obj is None:
                response['message'] = 'no user found with username'
                raise Exception('no user found with username  is required')
            
            
            
            send_reset_password_email(user_obj)
            
            
            response['status'] = 200
            response['message'] = 'An email is sent to you'
            
        
        except Exception as e:
            print(e)
            
        return Response(response)


ForgetPassword = ForgetPassword.as_view()


def verify_email(request , token):
    try:
        user_obj = User.objects.get(email_verification_token=  token)
        user_obj.is_verified = True
        user_obj.save()
        
    except Exception as e: 
        print(e)
        return JsonResponse({'status' : 500 , 'message' : 'Something went wrong'})
       
    return render(request, 'account_verified.html')
    
    

def change_password(request , token):
    context = {}

    try:
        user_obj = User.objects.get(forget_password_token=  token)
        context = {'user_id' : user_obj.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            user_id = request.POST.get('user_id')
            user_obj = User.objects.get(id=  user_id)
            user_obj.forget_password_token = None
            user_obj.set_password(new_password)
            user_obj.save()
            return JsonResponse({'status' : 200 , 'message' : 'Your password has been changed'})
            
        
    except Exception as e: 
        print(e)
        return JsonResponse({'status' : 500 , 'message' : 'Something went wrong'})
       
    return render(request, 'change_password.html' , context)
    
    