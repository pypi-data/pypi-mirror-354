from django.http import HttpResponse, JsonResponse # type: ignore
from .models import MaintenanceMode

class DynamicMaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path.startswith("/admin") or request.path.startswith("/api/admin"):
                return self.get_response(request)

            mode = MaintenanceMode.objects.first()
            if mode and mode.is_active:
                if request.user.is_authenticated and request.user.is_superuser:
                    return self.get_response(request)

                if request.path.startswith('/api') or 'application/json' in request.headers.get('Accept', ''):
                    return JsonResponse(
                        {"detail": "Service unavailable due to maintenance."},
                        status=503
                    )
                else:
                    return HttpResponse(
                        f"<h1>Maintenance Mode</h1><p>{mode.message}</p>",
                        content_type="text/html",
                        status=503
                    )
        except Exception:
            pass

        return self.get_response(request)