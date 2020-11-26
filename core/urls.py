from django.urls import path
from django.contrib.auth.models import User

from . import views

app_name = 'avic'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('lagout/', views.lagout, name='lagout'),
    path('register/', views.register, name='register')
]