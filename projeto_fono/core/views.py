
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from accounts.models import FonoUser
from accounts.models import PatientUser
from patients.models import PatientSessions
from patients.models import PatientTherapy


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

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        patients_count = PatientUser.objects.all().count()
        sessions_count = PatientSessions.objects.all().count()
        conduct_count = PatientTherapy.objects.all().count()

        context['patients_count'] = 0
        context['sessions_count'] = 0
        context['conduct_count'] = 0

        if patients_count:
            context['patients_count'] = patients_count
        if sessions_count:
            context['sessions_count'] = sessions_count
        if conduct_count:
            context['conduct_count'] = conduct_count

        return context

home = HomeView.as_view()