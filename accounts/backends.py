from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User




class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        username = email
        User = get_user_model()
        try:
            print(kwargs)
            email = kwargs.get('username')
            user = User.objects.get(Q(email__iexact=email))
            print(password)
            login(request , user)
        except Exception as e:
            print(e)
            User().set_password(password)
            return
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
