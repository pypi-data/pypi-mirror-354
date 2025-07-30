from django.db import models # type: ignore

class MaintenanceMode(models.Model):
    is_active = models.BooleanField(default=False)
    message = models.TextField(default="The site is under maintenance.")

    def __str__(self):
        return "ON" if self.is_active else "OFF"