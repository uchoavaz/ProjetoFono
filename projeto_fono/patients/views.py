
# -*- coding: utf-8 -*-
from .forms import PatientRegisterForm
from .models import PatientSessions
from .models import PatientSessionObjective
from .models import PatientSessionContent
from .models import PatientSessionActivity
from .models import PatientSessionObservation
from .models import PatientTherapy
from .models import PatientTherapyConduct
from .base_views import PatientPlanBaseView
from .base_views import PatientPlanSessionBaseView
from .base_views import PatientPlanSessionDeleteBaseView
from .base_views import PatientTherapyBaseView
from django.views.generic.edit import FormView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from accounts.models import PatientUser
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.db import IntegrityError


class PatientsListView(LoginRequiredMixin, ListView):
    template_name = 'patients_list.html'
    model = PatientUser

    def get_queryset(self):
        queryset = super(PatientsListView, self).get_queryset()
        queryset = queryset.filter(treater=self.request.user)

        return queryset


class PatientRegisterView(LoginRequiredMixin, FormView):
    template_name = 'patient_register.html'
    form_class = PatientRegisterForm
    success_url = '/pacientes/lista'

    def form_valid(self, form):
        form.instance.treater = self.request.user
        form.save()
        messages.success(self.request, 'Paciente cadastrado com sucesso')
        return super(PatientRegisterView, self).form_valid(form)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = PatientUser
    success_url = '/pacientes/lista'

    def get(self, *args, **kwargs):
        messages.success(
            self.request, 'Paciente deletado com sucesso com sucesso')
        return self.post(*args, **kwargs)


class PatientEditView(LoginRequiredMixin, FormView):
    template_name = 'patient_edit.html'
    form_class = PatientRegisterForm

    def get_form(self, form_class):
        patient = PatientUser.objects.get(id=self.kwargs.get('pk'))
        return form_class(instance=patient, **self.get_form_kwargs())

    def form_valid(self, form, **kwargs):
        form.save()
        context = self.get_context_data(**kwargs)
        context['form'] = form
        messages.success(self.request, 'Seu paciente foi atualizado')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(
            PatientEditView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['patient_name'] = PatientUser.objects.get(id=pk).nome
        context['pk_patient'] = self.kwargs.get('pk')
        context['patient_inform'] = True
        return context


class PatientPlanView(PatientPlanBaseView, ListView):
    template_name = 'patient_plan.html'

    def get_queryset(self):
        queryset = super(PatientPlanView, self).get_queryset()
        session = self.request.GET.get('obj')

        patient = PatientUser.objects.get(
            pk=self.kwargs.get('pk'))
        if session:
            try:
                queryset.create(
                    patient=patient,
                    sessao=session
                )
                messages.success(self.request, 'Sessão adicionada com sucesso')
            except IntegrityError:
                messages.error(self.request, u'Sessão já existente')
            except ValueError:
                messages.error(self.request, u'Apenas números')
        queryset = queryset.filter(
            patient=self.kwargs.get('pk')).order_by('sessao')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientPlanView, self).get_context_data(**kwargs)
        context['name_activity'] = u'Sessão'
        context['name_activity_plural'] = u'Sessões'
        return context


class PatientPlanSessionListView(PatientPlanBaseView, ListView):
    template_name = 'patient_plan_session_list.html'

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanSessionListView, self).get_context_data(**kwargs)
        context['session'] = self.kwargs.get('sessao')
        return context


class PatientPlanSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = PatientSessions

    def get(self, *args, **kwargs):
        messages.success(
            self.request, 'Sessão deletada com sucesso')
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        pk_patient = self.kwargs.get('pk')
        pk_sessao = self.kwargs.get('sessao')

        patient = PatientUser.objects.get(pk=pk_patient)

        query = self.get_queryset().get(sessao=pk_sessao, patient=patient)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:patient_plan',
                kwargs={
                    'pk': pk_patient}))


class PatientPlanSessionObjectiveView(PatientPlanSessionBaseView):
    model = PatientSessionObjective

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanSessionObjectiveView, self).get_context_data(**kwargs)
        context['session'] = self.kwargs.get('sessao')
        context['name_activity'] = 'Objetivo'
        context['objective'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:session_objective',
                kwargs={
                    'pk': self.kwargs.get('pk'),
                    'sessao': self.kwargs.get('sessao')
                }))
        else:
            return super(
                PatientPlanSessionObjectiveView, self).dispatch(
                request, *args, **kwargs)


class PatientPlanSessionObjectiveDeleteView(PatientPlanSessionDeleteBaseView):
    model = PatientSessionObjective

    def get(self, *args, **kwargs):
        messages.success(
            self.request, 'Deletado com sucesso')
        return self.post(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.pk_patient = self.kwargs.get('pk')
        self.pk_sessao = self.kwargs.get('sessao')
        self.pk_obj = self.kwargs.get('pk_obj')
        session = PatientSessions.objects.get(
            patient=self.pk_patient,
            sessao=self.pk_sessao)

        query = self.get_queryset().get(pk=self.pk_obj, session=session)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:session_objective',
                kwargs={
                    'pk': self.pk_patient,
                    'sessao': self.pk_sessao}))


class PatientPlanSessionContentView(PatientPlanSessionBaseView):
    model = PatientSessionContent

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanSessionContentView, self).get_context_data(**kwargs)
        context['session'] = self.kwargs.get('sessao')
        context['name_activity'] = u'Conteúdo'
        context['content'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:session_content',
                kwargs={
                    'pk': self.kwargs.get('pk'),
                    'sessao': self.kwargs.get('sessao')
                }))
        else:
            return super(
                PatientPlanSessionContentView, self).dispatch(
                request, *args, **kwargs)


class PatientPlanSessionContentDeleteView(PatientPlanSessionDeleteBaseView):
    model = PatientSessionContent

    def delete(self, request, *args, **kwargs):
        self.pk_patient = self.kwargs.get('pk')
        self.pk_sessao = self.kwargs.get('sessao')
        self.pk_obj = self.kwargs.get('pk_obj')
        session = PatientSessions.objects.get(
            patient=self.pk_patient,
            sessao=self.pk_sessao)

        query = self.get_queryset().get(pk=self.pk_obj, session=session)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:session_content',
                kwargs={
                    'pk': self.pk_patient,
                    'sessao': self.pk_sessao}))


class PatientPlanSessionActivityView(PatientPlanSessionBaseView):
    model = PatientSessionActivity

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanSessionActivityView, self).get_context_data(**kwargs)
        context['session'] = self.kwargs.get('sessao')
        context['name_activity'] = u'Atividade'
        context['activity'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:session_activity',
                kwargs={
                    'pk': self.kwargs.get('pk'),
                    'sessao': self.kwargs.get('sessao')
                }))
        else:
            return super(
                PatientPlanSessionActivityView, self).dispatch(
                request, *args, **kwargs)


class PatientPlanSessionActivityDeleteView(PatientPlanSessionDeleteBaseView):
    model = PatientSessionActivity

    def delete(self, request, *args, **kwargs):
        self.pk_patient = self.kwargs.get('pk')
        self.pk_sessao = self.kwargs.get('sessao')
        self.pk_obj = self.kwargs.get('pk_obj')
        session = PatientSessions.objects.get(
            patient=self.pk_patient,
            sessao=self.pk_sessao)

        query = self.get_queryset().get(pk=self.pk_obj, session=session)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:session_activity',
                kwargs={
                    'pk': self.pk_patient,
                    'sessao': self.pk_sessao}))


class PatientPlanSessionObservationView(PatientPlanSessionBaseView):
    model = PatientSessionObservation

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanSessionObservationView, self).get_context_data(**kwargs)
        context['session'] = self.kwargs.get('sessao')
        context['name_activity'] = u'Observação'
        context['observation'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:session_observation',
                kwargs={
                    'pk': self.kwargs.get('pk'),
                    'sessao': self.kwargs.get('sessao')
                }))
        else:
            return super(
                PatientPlanSessionObservationView, self).dispatch(
                request, *args, **kwargs)


class PatientPlanSessionObservationDeleteView(PatientPlanSessionDeleteBaseView):
    model = PatientSessionObservation

    def delete(self, request, *args, **kwargs):
        self.pk_patient = self.kwargs.get('pk')
        self.pk_sessao = self.kwargs.get('sessao')
        self.pk_obj = self.kwargs.get('pk_obj')
        session = PatientSessions.objects.get(
            patient=self.pk_patient,
            sessao=self.pk_sessao)

        query = self.get_queryset().get(pk=self.pk_obj, session=session)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:session_observation',
                kwargs={
                    'pk': self.pk_patient,
                    'sessao': self.pk_sessao}))


class PatientTherapyView(PatientTherapyBaseView, ListView):
    model = PatientTherapy
    template_name = 'patient_therapy.html'

    def get_queryset(self):
        queryset = super(PatientTherapyView, self).get_queryset()
        conduta = self.request.GET.get('obj')

        patient = PatientUser.objects.get(
            pk=self.kwargs.get('pk'))
        if conduta:
            try:
                queryset.create(
                    patient=patient,
                    conduta=conduta
                )
                messages.success(
                    self.request,
                    'Conduta fonoaudiológica adicionada com sucesso')
            except IntegrityError:
                messages.error(
                    self.request, u'Conduta fonoaudiológica já existente')
        queryset = queryset.filter(patient=patient)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientTherapyView, self).get_context_data(**kwargs)
        context['name_activity'] = u'Conduta Fonoaudiológica'
        context['name_activity_plural'] = u'Condutas Fonoaudiológicas'
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:patient_therapy',
                kwargs={
                    'pk': self.kwargs.get('pk')
                }))
        else:
            return super(
                PatientTherapyView, self).dispatch(
                request, *args, **kwargs)


class PatientTherapyDeleteView(LoginRequiredMixin, DeleteView):
    model = PatientTherapy

    def delete(self, request, *args, **kwargs):
        pk_patient = self.kwargs.get('pk')
        pk_conduta = self.kwargs.get('conduta')

        query = self.get_queryset().get(pk=pk_conduta)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:patient_therapy',
                kwargs={
                    'pk': pk_patient}))

    def get(self, *args, **kwargs):
        messages.success(
            self.request, 'Conduta Fonoaudiológica deletada com sucesso')
        return self.post(*args, **kwargs)


class PatientTherapyConductView(PatientTherapyBaseView, ListView):
    model = PatientTherapyConduct
    template_name = 'patient_therapy_conduct.html'

    def get_context_data(self, **kwargs):
        context = super(
            PatientTherapyConductView, self).get_context_data(**kwargs)
        context['conduct'] = PatientTherapy.objects.get(
            pk=self.kwargs.get('conduta')).conduta
        context['pk_conduct'] = self.kwargs.get('conduta')
        context['name_activity_plural'] = u'Tópicos'
        context['name_activity'] = u'Tópico'
        return context

    def get_queryset(self):
        queryset = super(PatientTherapyConductView, self).get_queryset()
        topico = self.request.GET.get('obj')

        conduta = PatientTherapy.objects.get(
            pk=self.kwargs.get('conduta'))
        if topico:
            try:
                queryset.create(
                    conduct=conduta,
                    descricao=topico
                )
                messages.success(
                    self.request,
                    'Tópico adicionado com sucesso')
            except IntegrityError:
                messages.error(
                    self.request, u'Tópico já existente')
        queryset = queryset.filter(conduct=conduta)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('obj'):
            self.get_queryset()
            return redirect(reverse_lazy(
                'patients:therapy_coduct',
                kwargs={
                    'pk': self.kwargs.get('pk'),
                    'conduta': self.kwargs.get('conduta')
                }))
        else:
            return super(
                PatientTherapyConductView, self).dispatch(
                request, *args, **kwargs)


class PatientTherapyConductTopicDeleteView(LoginRequiredMixin, DeleteView):
    model = PatientTherapyConduct

    def delete(self, request, *args, **kwargs):
        pk_patient = self.kwargs.get('pk')
        pk_conduta = self.kwargs.get('conduta')
        pk_topico = self.kwargs.get('topico')

        query = self.get_queryset().get(pk=pk_topico)
        query.delete()
        return HttpResponseRedirect(
            reverse(
                'patients:therapy_coduct',
                kwargs={
                    'pk': pk_patient,
                    'conduta': pk_conduta}))

    def get(self, *args, **kwargs):
        messages.success(
            self.request, u'Tópico deletado com sucesso')
        return self.post(*args, **kwargs)


topic_delete = PatientTherapyConductTopicDeleteView.as_view()
therapy_coduct = PatientTherapyConductView.as_view()
therapy_delete = PatientTherapyDeleteView.as_view()
patient_therapy = PatientTherapyView.as_view()
activity_delete = PatientPlanSessionActivityDeleteView.as_view()
session_activity = PatientPlanSessionActivityView.as_view()
observation_delete = PatientPlanSessionObservationDeleteView.as_view()
session_observation = PatientPlanSessionObservationView.as_view()
content_delete = PatientPlanSessionContentDeleteView.as_view()
session_content = PatientPlanSessionContentView.as_view()
objective_delete = PatientPlanSessionObjectiveDeleteView.as_view()
session_objective = PatientPlanSessionObjectiveView.as_view()
session_list = PatientPlanSessionListView.as_view()
session_delete = PatientPlanSessionDeleteView.as_view()
patient_plan = PatientPlanView.as_view()
patient_edit = PatientEditView.as_view()
patient_delete = PatientDeleteView.as_view()
patient_register = PatientRegisterView.as_view()
patients_list = PatientsListView.as_view()
