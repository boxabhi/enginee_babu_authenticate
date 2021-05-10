from rest_framework import serializers
# from .models import *
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from .thread import *
import uuid
from rest_framework.validators import UniqueValidator





class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    
    

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
        
    
    
        