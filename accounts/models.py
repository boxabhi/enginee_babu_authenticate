from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from .manager import UserManager
from .thread import SendAccountActivationEmail , SendForgetPasswordEmail
from django.contrib.auth.signals import user_logged_in, user_logged_out 
import datetime




class User(AbstractUser):
    username = None
    email = models.EmailField( unique=True)
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email


class ForgetPassword(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email















'''  ALL SIGNALS HERE  '''


@receiver(user_logged_in) 
def _user_logged_in(sender , user,request, **kwargs):
    try:
        user.last_login_time = datetime.datetime.now()
        user.save()
    except Exception as e: 
        print(e)

@receiver(user_logged_out) 
def _user_logged_out(sender , user,request, **kwargs):
    try:
        user.last_logout_time = datetime.datetime.now()
        user.save()
    except Exception as e: 
        print(e)



@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_verification_token = str(uuid.uuid4())
            instance.email_verification_token = email_verification_token
            ''' EXCEUTING THREAD TO SEND EMAIL '''
            SendAccountActivationEmail(instance.email , email_verification_token).start()

    except Exception as e:
        print(e)
        
@receiver(post_save, sender=ForgetPassword)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            ''' EXCEUTING THREAD TO SEND EMAIL '''

            SendForgetPasswordEmail(instance.user.email , instance.forget_password_token).start()

    except Exception as e:
        print(e)
