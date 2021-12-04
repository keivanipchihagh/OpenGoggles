from django.forms import ModelForm
from .models import *


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email_address', 'password']