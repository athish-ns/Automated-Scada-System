# main/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adminconsole/', include('adminconsole.urls')),
    # other app-specific URLs go here
]
