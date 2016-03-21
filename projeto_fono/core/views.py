
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from accounts.models import FonoUser


def login(request):

    context = {}

    enrollment = request.POST.get('username')
    password = request.POST.get('password')

    context['user_label'] = FonoUser._meta.get_field(
        "enrollment").verbose_name.title()
    context['password_label'] = FonoUser._meta.get_field(
        "password").verbose_name.title()
    context['user_not_active'] = False
    context['user_does_not_exists'] = False

    if enrollment and password:
        user = authenticate(enrollment=enrollment, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                context['user_not_active'] = True
        else:
            context['user_does_not_exists'] = True
    return render(request, 'login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/login')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    login_url = '/login'


home = HomeView.as_view()