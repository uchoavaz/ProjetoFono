
from django.contrib import admin
from .models import PatientSessions
from .models import PatientSessionObjective
from .models import PatientSessionContent
from .models import PatientSessionActivity
from .models import PatientSessionObservation


class BaseSessionAdmin(admin.ModelAdmin):
    list_filter = ['session']
    list_display = (
        'session', 'descricao')


class PatientSessionAdmin(admin.ModelAdmin):
    list_filter = ['sessao']
    list_display = (
        'sessao', 'patient')


class PatientSessionObjectiveAdmin(BaseSessionAdmin):
    pass


class PatientSessionActivitiesAdmin(BaseSessionAdmin):
    pass


class PatientSessionContentAdmin(BaseSessionAdmin):
    pass


class PatientSessionObservationsAdmin(BaseSessionAdmin):
    pass


admin.site.register(
    PatientSessionObservation, PatientSessionObservationsAdmin)
admin.site.register(PatientSessionContent, PatientSessionContentAdmin)
admin.site.register(PatientSessionActivity, PatientSessionActivitiesAdmin)
admin.site.register(PatientSessionObjective, PatientSessionObjectiveAdmin)
admin.site.register(PatientSessions, PatientSessionAdmin)
