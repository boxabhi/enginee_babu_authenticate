from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from .thread import *

# class User(AbstractUser):

#     def name(self):
#         return self.first_name + ' ' + self.last_name


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField( unique=True)

    is_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=200 , null=True, blank=True)
    forget_password_token = models.CharField(max_length=200 ,null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def name(self):
        return self.first_name + ' ' + self.last_name





@receiver(post_save, sender=CustomUser)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_verification_token = str(uuid.uuid4())
            instance.email_verification_token = email_verification_token
            SendAccountActivationEmail(instance.email , email_verification_token).start()

    except Exception as e:
        print(e)
