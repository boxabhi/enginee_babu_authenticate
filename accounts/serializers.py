from rest_framework import serializers
# from .models import *
from django.contrib.auth import authenticate, get_user_model
User = get_user_model()
from .thread import *
import uuid
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super(MyTokenObtainSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField()

    def validate(self, attrs):
        # self.user = authenticate(**{
        #     self.username_field: attrs[self.username_field],
        #     'password': attrs['password'],
        # })
        self.user = User.objects.filter(email=attrs[self.username_field]).first()
        print(self.user)

        if not self.user:
            raise Exception('The user is not valid.')

        if self.user:
            if not self.user.check_password(attrs['password']):
                raise Exception('Incorrect credentials.')
        print(self.user)
        if self.user is None or not self.user.is_active:
            raise Exception('No active account found with the given credentials')


        refresh = RefreshToken.for_user(self.user)
        print('@@@')
        print(refresh)
        print('@@@')
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    @classmethod
    def get_token(cls, user):
        raise NotImplemented(
            'Must implement `get_token` method for `MyTokenObtainSerializer` subclasses')




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
        
    
    
        