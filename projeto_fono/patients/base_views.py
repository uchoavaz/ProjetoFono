
from django.contrib import messages
from .models import PatientSessions
from accounts.models import PatientUser
from django.views.generic import DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class PatientPlanBaseView(LoginRequiredMixin):
    model = PatientSessions

    def get_context_data(self, **kwargs):
        context = super(
            PatientPlanBaseView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['patient_name'] = PatientUser.objects.get(id=pk).nome
        context['hip_diag'] = PatientUser.objects.get(
            id=pk).hipotese_diagnostico
        context['pk_patient'] = self.kwargs.get('pk')
        context['patient_plan'] = True
        return context


class PatientPlanSessionBaseView(PatientPlanBaseView, ListView):
    template_name = 'patient_plan_session_schedules.html'

    def get_queryset(self):
        queryset = super(PatientPlanSessionBaseView, self).get_queryset()
        objetivo = self.request.GET.get('obj')

        session = PatientSessions.objects.get(
            patient=self.kwargs.get('pk'),
            sessao=self.kwargs.get('sessao'))

        if objetivo:
            queryset.create(
                session=session,
                descricao=objetivo)

        queryset = queryset.filter(session=session)
        return queryset


class PatientPlanSessionDeleteBaseView(LoginRequiredMixin, DeleteView):
    pk_sessao = None
    pk_obj = None
    pk_patient = None

    def get(self, *args, **kwargs):
        messages.success(
            self.request, 'Deletado com sucesso')
        return self.post(*args, **kwargs)


class PatientTherapyBaseView(LoginRequiredMixin):

    def get_context_data(self, **kwargs):
        context = super(
            PatientTherapyBaseView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['patient_name'] = PatientUser.objects.get(id=pk).nome
        context['hip_diag'] = PatientUser.objects.get(
            id=pk).hipotese_diagnostico
        context['pk_patient'] = self.kwargs.get('pk')
        context['patient_therapy'] = True
        return context