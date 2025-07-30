from django.contrib import admin # type: ignore
from .models import MaintenanceMode

admin.site.register(MaintenanceMode)