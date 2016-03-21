from django.contrib import admin
from .models import FonoUser

class FonoUserAdmin(admin.ModelAdmin):
    list_filter = ['enrollment']
    list_display = (
        'enrollment', 'username', 'email', 'is_staff',
        'is_active', 'is_superuser')
admin.site.register(FonoUser, FonoUserAdmin)