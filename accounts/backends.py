from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout


UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        username = email
        try:
            username = (kwargs.get('username'))
            # user_obj = authenticate(email = username , password = password)
            # print(user_obj)
            # login(request , user_obj)
            user = UserModel.objects.get(Q(email__iexact=username))
            print(password)
            login(request , user)
        except Exception as e:
            print(e)
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
