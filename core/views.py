from django.contrib import auth
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Course, Usercourse


def index(request):
    if request.user.is_authenticated:
        context = {}
        context['user'] = request.user.username
        context['usercourses'] = []
        objects = Usercourse.objects.filter(user_name=request.user)
        
        for i in objects:
            context['usercourses'].append((i.course.course_name, i.scores))
        
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

def choose(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('avic:login'))
        
    if request.method == 'POST':
        chosen_courses = request.POST.getlist('courses')
        print(chosen_courses)
        print("fucls")

        for i in chosen_courses:
            course = Course.objects.get(course_name=i)
            user_course = Usercourse.objects.create(user_name=request.user, course=course)
            user_course.save()
        
        return HttpResponseRedirect(reverse('avic:index'))
    
    has_chosen = set([x.course.pk for x in Usercourse.objects.filter(user_name=request.user)])
    not_chosen = []
    print("hah")
    print(has_chosen)

    all_courses = Course.objects.all()

    for course in all_courses:
        print(course.pk)
        if course.pk not in has_chosen:
            not_chosen.append(course)
            print(not_chosen)
    
    context = {}
    context['list'] = not_chosen

    return render(request, "core/choose.html", context)

