from rest_framework import serializers
from django.contrib.auth import  get_user_model
User = get_user_model()
from rest_framework.validators import UniqueValidator
from .models import ForgetPassword
import uuid




class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()
    
    

class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'
        


class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'email' , 'password']
        
    def create(self , validated_data):
        user = User.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    
    def forget_password(self , instance , validated_data):
        
        email = validated_data['email']
        
        print(email)
    
    
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = '__all__'
        
    
    def create(self , validated_data):
        print(validated_data)
        user = User.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['email' , 'password']
  
        
    
           
        

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    class Meta:
        model = ForgetPassword
        fields = ['token' , 'password']
        
    def change_password(self):
        validated_data = self.validated_data
        forget_password_obj =  None
        print(validated_data['token'])
        try:
            forget_password_obj = ForgetPassword.objects.get(forget_password_token=validated_data['token'])
        except Exception as e:
            raise serializers.ValidationError("invalid token")
        
        user_obj = User.objects.get(id = forget_password_obj.user.id)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        
        return True
        

class ForgetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['email']    
        
    def forget_password(self):
        email = self.validated_data['email']
        user_obj = None
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("invalid email user not found")
        
        token = str(uuid.uuid4())
        ForgetPassword.objects.create(user = user_obj ,forget_password_token = token )
        return True
        
        