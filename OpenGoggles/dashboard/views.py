from django.urls import reverse
from django.contrib.auth import login, logout
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'dashboard/index.html', context = {})


def loginView(request):

    # Capture the form data if exists
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        user = form.login(request)  # Authenticate the user        
        if user:
            # Login the user and redirect to the dashboard       
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard:index'))
        else:
            # Return the form with errors
            return render(request, 'dashboard/login.html', context = { 'form': form, 'error_message': 'Incorrect Email/Password' })

    return render(request, 'dashboard/login.html', context = { 'form': form })


@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('dashboard:login'))


def registerView(request):
    return render(request, 'dashboard/register.html', context = {
        'form': RegisterForm(),
    })