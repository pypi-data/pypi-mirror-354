from django.apps import AppConfig # type: ignore

class DynamicMaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dynamic_maintenance'