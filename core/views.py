from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Usercourse


def index(request):
    if request.user.is_authenticated:
        context = {}
        context['user'] = request.user.username
        context['usercourses'] = []
        objects = Usercourse.objects.filter(user_name=request.user)
        
        for i in objects:
            context['usercourses'].append((i.user_name.username, i.course.course_name))
        
        return render(request, 'core/index.html', context)
    else:
        return HttpResponseRedirect(reverse('avic:login'))


def login(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('avic:index'))
            else:
                return render(request, 'core/login.html', {'messages': 'please relogin'})
    else:
        return render(request, "core/login.html")

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.create_user(
                username=username, password=password)
            user.save()
            if user:
                auth.logout(request)
                auth.login(request, user)
            return HttpResponseRedirect(reverse('avic:index'))
        except:
            return render(request, 'core/register.html', {'messages': '用户名已注册，请重新注册'})
    else:
        return render(request, 'core/register.html')

def lagout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('avic:index'))