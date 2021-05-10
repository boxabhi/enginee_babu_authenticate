import threading
from django.conf import settings
from django.core.mail import send_mail


class SendAccountActivationEmail(threading.Thread):
    
    def __init__(self , email , token):
        self.email = email
        self.token = token
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = 'Your email verification link '
            message = f'Hi , click on the link to activate your password http://127.0.0.1:8000/api/accounts/verify/{self.token}/'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.email]
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(e)
            


class SendForgetPasswordEmail(threading.Thread):
    
    def __init__(self , email , token):
        self.email = email
        self.token = token
        threading.Thread.__init__(self)
    
    def run(self):
        try:
            subject = 'Your forget password link'
            message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/api/accounts/change-password/{self.token}/'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [self.email]
            send_mail(subject, message, email_from, recipient_list)
        except Exception as e:
            print(e)