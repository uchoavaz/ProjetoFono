
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db import models


class FonoUserManager(BaseUserManager):
    def create_user(self, enrollment,
                    username,
                    email,
                    password=None):
        user = self.model(
            enrollment=enrollment, username=username, email=email)
        user.set_password(password)
        user.is_active = True
        return user

    def create_superuser(self, enrollment, username, email,
                         password):
        user = self.create_user(enrollment=enrollment,
                                username=username,
                                email=email,
                                password=password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True

        user.save()
        return user


class FonoUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="Nome do usuário", max_length=50, unique=True)
    email = models.EmailField(
        verbose_name=(u'E-mail'),
        max_length=255,
        unique=True,
        db_index=True,
        null=True,
        blank=True)
    enrollment = models.CharField(
        max_length=20, unique=True, verbose_name='Matrícula')

    supervisor = models.CharField(
        max_length=100, verbose_name="Supervisor")
    is_staff = models.BooleanField(
        verbose_name=('Status de suporte'), default=False)

    is_active = models.BooleanField(
        verbose_name=(u'ativo'), default=True)
    full_name = models.CharField(
        verbose_name='Nome completo', max_length=100)

    short_name = models.CharField(
        verbose_name='Nome abreviado', max_length=50)

    created_at = models.DateTimeField(
        verbose_name=(u'data de inscrição'), default=timezone.now)

    updated_at = models.DateTimeField(
        verbose_name=(u'última atualização'),
        default=timezone.now)

    objects = FonoUserManager()

    USERNAME_FIELD = 'enrollment'
    REQUIRED_FIELDS = ['email', 'username']

    class Meta:
        verbose_name = (u'usuário')
        verbose_name_plural = (u'usuários')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.short_name

    def __str__(self):
        return self.enrollment


class PatientUser(models.Model):

    treater = models.ForeignKey(
        FonoUser, related_name='paciente', verbose_name="Tratador")
    nome = models.CharField(verbose_name='Nome', max_length=100)
    identidade = models.CharField(
        verbose_name='Identidade', max_length=15, unique=True)
    cpf = models.CharField(
        verbose_name='CPF', max_length=20, unique=True)
    idate = models.IntegerField(verbose_name='Idade')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    naturalidade = models.CharField(
        verbose_name='Naturalidade', max_length=30,
        null=True, blank=True)
    profissao = models.CharField(
        verbose_name=u'Profissão', max_length=30,
        null=True, blank=True)
    estado_civil = models.CharField(
        verbose_name='Estado Civil', max_length=20,
        null=True, blank=True)
    pai = models.CharField(
        verbose_name='Pai', max_length=100,
        null=True, blank=True)
    mae = models.CharField(
        verbose_name=u'Mãe', max_length=100,
        null=True, blank=True)
    escolaridade = models.CharField(
        verbose_name='Escolaridade',
        max_length=30, null=True, blank=True)
    endereco = models.CharField(
        verbose_name=u'Endereço', max_length=255, null=True, blank=True)
    bairro = models.CharField(
        verbose_name='Bairro', max_length=50, null=True, blank=True)
    cep = models.CharField(
        verbose_name='CEP', max_length=10, null=True,
        blank=True)
    fone = models.CharField(
        verbose_name='Telefone', max_length=20, null=True,
        blank=True)
    contato = models.CharField(
        verbose_name='Contato', max_length=100, null=True,
        blank=True)
    encaminhado_por = models.CharField(
        verbose_name='Encaminhado por', max_length=100)
    hipostese_diagnostico = models.CharField(
        verbose_name=u'Hipótese de Diagnóstico', max_length=100, null=True,
        blank=True)
    motivo_consulta = models.TextField(
        verbose_name='Motivo da Consulta',
        null=True, blank=True)
    autorizacao = models.CharField(verbose_name=u'Autorização', max_length=50)
    valor_sessao = models.FloatField(verbose_name=u'Valor da Sessão')
    desconto = models.FloatField(verbose_name='Desconto')
    inicio_atentimento = models.DateField(
        verbose_name=u'Início do Atendimento')
    termino_atendimento = models.DateField(
        verbose_name=u'Término do Atendimento', null=True, blank=True)

    class Meta:
        verbose_name = (u'paciente')
        verbose_name_plural = (u'pacientes')

    def __str__(self):
        return self.nome
