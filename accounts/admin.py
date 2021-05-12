from django.contrib import admin
from .models import User,ForgetPassword

admin.site.register(User)
admin.site.register(ForgetPassword)