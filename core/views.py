from avic.settings import REGISTER_ID_FAIL
from django.conf import settings
from django.contrib import auth
from django.core.validators import validate_email
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import College, Course, User, Usercourse


def index(request):
    context = {}

    if request.user.is_authenticated:
        context['user'] = request.user.username
        context['usercourses'] = []

        for i in Usercourse.objects.filter(user_name=request.user):
            context['usercourses'].append((i.course.course_name,
                                           i.course.teacher_name,
                                           i.course.course_scores,
                                           i.course.semester,
                                           i.scores))
    else:
        return HttpResponseRedirect(reverse('avic:login'))
    return render(request, 'core/index.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('avic:index'))
        else:
            return render(request, 'core/login.html', {'messages': settings.LOGIN_FAIL_MSG})
    else:
        return render(request, "core/login.html")


def register(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        if username > settings.MAX_STUDENT_ID or username < settings.MIN_STUDENT_ID:
            context['messages'] = REGISTER_ID_FAIL
            context['college'] = [
                x.college_name for x in College.objects.all()]
            return render(request, 'core/register.html', context)

        password = request.POST.get('password')

        email = request.POST.get('email')
        try:
            validate_email(email)
        except:
            context['messages'] = settings.REGISTER_EMAIL_FAIL
            context['college'] = [
                x.college_name for x in College.objects.all()]
            return render(request, 'core/register.html', context)

        try:
            college = College.objects.get(
                college_name=request.POST.get('college'))
        except:
            context['messages'] = settings.REGISTER_COLLEGE_FAIL
            context['college'] = [
                x.college_name for x in College.objects.all()]
            return render(request, 'core/register.html', context)

        try:
            user = User.objects.create_user(
                username=username, password=password, email=email, college=college)
            user.save()

            if user:
                auth.logout(request)
                auth.login(request, user)
                return HttpResponseRedirect(reverse('avic:index'))
        except:
            context['messages'] = settings.REGISTER_NAME_FAIL
            context['college'] = [
                x.college_name for x in College.objects.all()]
            return render(request, 'core/register.html', context)

    else:
        context['college'] = [x.college_name for x in College.objects.all()]
        return render(request, 'core/register.html', context)


def lagout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('avic:index'))


def choose(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('avic:login'))

    if request.method == 'POST':
        chosen_course_name = request.POST.get('course')
        course = Course.objects.get(course_name=chosen_course_name)
        user_course = Usercourse.objects.create(
            user_name=request.user, course=course)
        user_course.save()

    has_chosen = set(
        [x.course.pk for x in Usercourse.objects.filter(user_name=request.user)])
    not_chosen = []
    all_courses = Course.objects.all()
    for course in all_courses:
        if course.pk not in has_chosen:
            not_chosen.append(course)
    return render(request, "core/choose.html", {'list': not_chosen})
