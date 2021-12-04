from django import forms
from django.contrib.auth import authenticate
from django.forms import Form
from .models import *


class RegisterForm(Form):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginForm(Form):
    email = forms.EmailField(required = True, label = 'Email Address')
    password = forms.CharField(widget = forms.PasswordInput())

    fields = ['email', 'password']
    
    def login(self, request):
        return authenticate(username = self.cleaned_data['email'], password = self.cleaned_data['password'])