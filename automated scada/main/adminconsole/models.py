# yourappname/models.py

from django.db import models

class SystemSettings(models.Model):
    ph_lower_limit = models.FloatField(default=5.0)
    ph_upper_limit = models.FloatField(default=7.0)
    control_system_status = models.BooleanField(default=False)
    monitoring_system_status = models.BooleanField(default=False)

    def __str__(self):
        return "System Settings"
