from django.db import connections
from django.http import HttpResponse, JsonResponse


def health(request):
    try:
        connections['default'].cursor().execute('SELECT 1')
        db_ok = True
    except Exception:
        db_ok = False
    status = 200 if db_ok else 503
    return JsonResponse({'status': 'ok' if db_ok else 'degraded', 'db': db_ok}, status=status)


def healthz(request):
    return HttpResponse('ok')
