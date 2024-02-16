# yourappname/admin.py

from django.contrib import admin
from .models import SystemSettings
from subprocess import Popen

class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ('ph_lower_limit', 'ph_upper_limit', 'control_system_status', 'monitoring_system_status')
    actions = ['start_control_system', 'start_monitoring_system']

    def start_control_system(self, request, queryset):
        # Code to start the control system
        Popen(["python", ".control_system.py"])

    def start_monitoring_system(self, request, queryset):
        # Code to start the monitoring system
        Popen(["python", ".monitoring.py"])

admin.site.register(SystemSettings, SystemSettingsAdmin)
