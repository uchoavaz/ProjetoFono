
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from accounts.models import PatientUser
from django.db import models


class PatientSessions(models.Model):
    patient = models.ForeignKey(
        PatientUser,
        related_name="planejamento_diario",
        on_delete=models.CASCADE)
    sessao = models.IntegerField(verbose_name=u"Número da sessão")

    class Meta:
        unique_together = (("patient", "sessao"),)
        verbose_name = (u'sessão do paciente')
        verbose_name_plural = (u'sessões do paciente')

    def __repr__(self):
        return self.patient + " " + self.sessao

    def __str__(self):
        return str(self.sessao)


class PatientSessionObjective(models.Model):
    session = models.ForeignKey(
        PatientSessions,
        related_name="objetivo",
        on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        verbose_name = (u'Objetivo da sessão')
        verbose_name_plural = (u'Objetivos da sessão')


class PatientSessionContent(models.Model):
    session = models.ForeignKey(
        PatientSessions,
        related_name="conteudo",
        on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        verbose_name = (u'Conteudo da sessão')
        verbose_name_plural = (u'Conteudos da sessão')


class PatientSessionActivity(models.Model):
    session = models.ForeignKey(
        PatientSessions,
        related_name="atividade",
        on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        verbose_name = (u'Atividade da sessão')
        verbose_name_plural = (u'Atividades da sessão')


class PatientSessionObservation(models.Model):
    session = models.ForeignKey(
        PatientSessions,
        related_name="observacao",
        on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        verbose_name = (u'Observação da sessão')
        verbose_name_plural = (u'Observações da sessão')


class PatientTherapy(models.Model):
    patient = models.ForeignKey(
        PatientUser,
        related_name="planejamento_terapeutico",
        on_delete=models.CASCADE)
    conduta = models.TextField(
        verbose_name=u'Conduta terapêutica', unique=True)

    class Meta:
        unique_together = (("patient", "conduta"),)
        verbose_name = (u'Planejamento terapêutico')
        verbose_name_plural = (u'Planejamentos terapêuticos')


class PatientTherapyConduct(models.Model):
    conduct = models.ForeignKey(
        PatientTherapy,
        related_name="conduta_fonoaudiologica",
        on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name=u'Descrição')

    class Meta:
        verbose_name = (u'Conduta Fonoaudiológica')
        verbose_name_plural = (u'Condutas Fonoaudiológicas')