
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

    def __init__(self, *args, **kwargs):
        super(PatientRegisterForm, self).__init__(*args, **kwargs)
        self.fields['data_nascimento'].widget.attrs\
            .update({
                'id': 'data_nascimento',
                'type': 'text'
            })
        self.fields['inicio_atendimento'].widget.attrs\
            .update({
                'id': 'inicio_atendimento',
                'type': 'text'
            })
        self.fields['termino_atendimento'].widget.attrs\
            .update({
                'id': 'termino_atendimento',
                'type': 'text'
            })
        self.fields['cep'].widget.attrs\
            .update({
                'maxlength': '9',
                'OnKeyPress': "formatar('#####-###', this)"
            })
        self.fields['cpf'].widget.attrs\
            .update({
                'maxlength': '14',
                'OnKeyPress': "formatar('###.###.###-##', this)"
            })

class PatientPlanForm(PatientBaseForm):
    class Meta:
        model = PatientUser
        exclude = ['treater']


class PatientPlanSessionRegisterForm(PatientBaseForm):
    class Meta:
        model = PatientSessions
        fields = ['sessao']
