from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import LoginForm, RegisterForm

def index(request):
    return HttpResponse("Hello, world. You're at the dashboard index.")


def login(request):
    return render(request, 'dashboard/login.html', context = {
        'form': LoginForm()
    })

def register(request):
    return render(request, 'dashboard/register.html', context = {
        'form': RegisterForm()
    })