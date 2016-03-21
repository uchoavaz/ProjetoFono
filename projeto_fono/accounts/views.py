from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from .forms import PasswordForm
from .models import FonoUser


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/conta/perfil'

    def get_form(self, form_class):
        user = FonoUser.objects.get(enrollment=self.request.user.enrollment)
        return form_class(instance=user, **self.get_form_kwargs())

    def form_valid(self, form, **kwargs):
        form.instance.user = self.request.user
        form.save()
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['salvo'] = True
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ProfileView,
                        self).get_context_data(**kwargs)
        context['salvo'] = False
        return context


class PasswordView(LoginRequiredMixin, FormView):
    template_name = 'password.html'
    form_class = PasswordForm
    success_url = '/'
    def get_form(self, form_class):
        user = FonoUser.objects.get(enrollment=self.request.user.enrollment)
        return form_class(instance=user, **self.get_form_kwargs())
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(PasswordView, self).form_valid(form)
profile = ProfileView.as_view()
password = PasswordView.as_view()
