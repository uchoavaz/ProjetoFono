
# -*- coding: utf-8 -*-
from django import forms
from accounts.models import PatientUser
from .models import PatientSessions

class PatientBaseForm(forms.ModelForm):

    def save(self, commit=True):
        user = super(PatientBaseForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class PatientRegisterForm(PatientBaseForm):
    class Meta:
        model = PatientUser
        exclude = ['treater']


class PatientPlanForm(PatientBaseForm):
    class Meta:
        model = PatientUser
        exclude = ['treater']


class PatientPlanSessionRegisterForm(PatientBaseForm):
    class Meta:
        model = PatientSessions
        fields = ['sessao']
