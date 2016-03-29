from django.contrib import admin
from .models import FonoUser
from .models import PatientUser


class FonoUserAdmin(admin.ModelAdmin):
    list_filter = ['enrollment']
    list_display = (
        'enrollment', 'username', 'email', 'is_staff',
        'is_active', 'is_superuser')


class PatientAdmin(admin.ModelAdmin):
    list_filter = ['identidade']
    list_display = (
        'nome', 'identidade', 'cpf', 'treater')

admin.site.register(PatientUser, PatientAdmin)
admin.site.register(FonoUser, FonoUserAdmin)
