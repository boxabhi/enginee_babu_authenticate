from django.core.mail import send_mail
from django.conf import settings 
import uuid
from .thread import *





def send_reset_password_email(user_obj):
    try:
        token = str(uuid.uuid4())
        user_obj.forget_password_token = token
        user_obj.save()
        SendForgetPasswordEmail(user_obj.email , token).start()
    except Exception as e:
        print(e)
        
            
    


def send_email_verification_mail(email , token ):
    subject = 'Your email verification link '
    message = f'Hi , click on the link to activate your password http://127.0.0.1:8000/accounts/verify/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True




def send_forget_password_mail(email , token ):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
