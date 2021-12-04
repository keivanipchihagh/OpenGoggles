from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path('register/', views.registerView, name = 'register'),
]