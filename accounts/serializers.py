from rest_framework import serializers
from django.contrib.auth import  get_user_model
User = get_user_model()
from rest_framework.validators import UniqueValidator
from .models import ForgetPassword




class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    token = serializers.CharField()
    
    

class ResetPasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'
        


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
    
        
        

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    

    def create(self , validated_data):
        user = User.objects.create(email = validated_data['email'])
        user.set_password(validated_data['password'])
        return user
        
        
        