from django.conf import settings
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class AgeGateMiddleware(MiddlewareMixin):
    """Додає прапор show_age_gate; блокує контент лише на рівні шаблону/JS."""

    SKIP_PREFIXES = (
        '/static/', '/media/', '/api/', '/i18n/', '/htmx/',
    )

    def process_request(self, request):
        admin_prefix = f'/{settings.ADMIN_URL.strip("/")}'
        path = request.path
        if path.startswith(admin_prefix) or any(path.startswith(p) for p in self.SKIP_PREFIXES):
            request.show_age_gate = False
            request.age_denied = False
            return None

        cookie = request.COOKIES.get(settings.AGE_GATE_COOKIE)
        request.age_denied = cookie == '0'
        request.show_age_gate = cookie not in ('1', '0')
        return None
