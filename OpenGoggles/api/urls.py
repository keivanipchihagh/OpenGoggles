from django.urls import path
from .views import *

urlpatterns = [
    path('index/<str:username>', index, name='index'),
]
