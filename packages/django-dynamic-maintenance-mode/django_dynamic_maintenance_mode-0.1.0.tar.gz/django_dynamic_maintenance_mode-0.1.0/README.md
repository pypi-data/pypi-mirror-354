# django-dynamic-maintenance-mode

Django middleware to enable maintenance mode dynamically using a database flag. Works for both web views and Django REST Framework APIs.

## Features

- Toggle maintenance mode from the admin panel
- Superusers can bypass maintenance restrictions
- Admin routes are always accessible

## Installation

```bash
pip install django-dynamic-maintenance-mode
```

## Configuration

Add to `INSTALLED_APPS` in settings.py:

```python
'dynamic_maintenance',
```

Add to MIDDLEWARE near the top:

```python
'dynamic_maintenance.middleware.DynamicMaintenanceMiddleware',
```

Run migrations:

```bash
python manage.py migrate
```

Use the admin panel to toggle maintenance mode.## Usage

### Enable or Disable Maintenance Mode

You can toggle the maintenance mode from the Django Admin panel or using Django shell:

```bash
python manage.py shell
```

Then in shell:

```python
from dynamic_maintenance.models import MaintenanceMode
mode, created = MaintenanceMode.objects.get_or_create(id=1)
mode.is_active = True  # or False to disable
mode.message = "We are performing scheduled maintenance. Please check back soon."
mode.save()
```

Alternatively, you can create a custom Django management command for enabling/disabling maintenance mode.

### Enable or Disable Maintenance Mode CMD

Commands to enable/disable maintenance mode dynamically

    ```bash
    python manage.py maintenance_mode on
    python manage.py maintenance_mode off
    ```

## License

MIT

---