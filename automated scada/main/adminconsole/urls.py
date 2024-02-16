# adminconsole/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('adjust-ph-level/', views.adjust_ph_level, name='adjust_ph_level'),
    path('start-control-system/', views.start_control_system, name='start_control_system'),
    path('stop-control-system/', views.stop_control_system, name='stop_control_system'),
    path('start-monitoring-system/', views.start_monitoring_system, name='start_monitoring_system'),
    path('stop-monitoring-system/', views.stop_monitoring_system, name='stop_monitoring_system'),
    # Add more URLs as needed
]
