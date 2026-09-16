"""Language switcher compatible with prefix_default_language=False.

Django's set_language uses translate_url(), which resolve()s the current path
in the active language. LocaleMiddleware forces LANGUAGE_CODE on unprefixed
/i18n/setlang/, so /en/... and /zh-hans/... do not resolve and the redirect
keeps the old prefix. URL prefix then wins over the language cookie.
"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language
from django.views.i18n import LANGUAGE_QUERY_PARAMETER

from apps.core.templatetags.rs_i18n import localize_path_for


def set_language(request):
    next_url = request.POST.get('next', request.GET.get('next'))
    if (
        next_url or request.accepts('text/html')
    ) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get('HTTP_REFERER')
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = '/'

    lang_code = None
    if request.method == 'POST':
        posted = request.POST.get(LANGUAGE_QUERY_PARAMETER)
        if posted and check_for_language(posted):
            lang_code = posted

    if next_url and lang_code:
        next_url = localize_path_for(next_url, lang_code)

    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)
    if request.method == 'POST' and lang_code:
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response
