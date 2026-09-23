from __future__ import annotations

import json

from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.pwa.models import PushSubscription
from apps.pwa.services.catalog_snapshot import build_catalog_snapshot
from apps.pwa.services.push import vapid_configured, vapid_public_key


def _normalize_lang(raw: str) -> str:
    allowed = {code for code, _ in settings.LANGUAGES}
    lang = (raw or '').strip().lower().replace('_', '-')
    if lang in allowed:
        return lang
    base = lang.split('-', 1)[0]
    for code in allowed:
        if code == base or code.startswith(f'{base}-'):
            return code
    return settings.LANGUAGE_CODE


@require_GET
def manifest(request):
    name = 'Royal Smoke'
    try:
        from apps.core.models import SiteSettings

        name = SiteSettings.load().site_name or name
    except Exception:
        pass
    data = {
        'name': name,
        'short_name': 'RoyalSmoke',
        'description': 'Сигари та аксесуари Royal Smoke',
        'start_url': '/?utm_source=pwa',
        'scope': '/',
        'display': 'standalone',
        'orientation': 'portrait-primary',
        'background_color': '#100d0c',
        'theme_color': '#100d0c',
        'lang': 'uk',
        'dir': 'ltr',
        'icons': [
            {
                'src': f'{settings.STATIC_URL}img/pwa-192.png',
                'sizes': '192x192',
                'type': 'image/png',
                'purpose': 'any',
            },
            {
                'src': f'{settings.STATIC_URL}img/pwa-512.png',
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'any',
            },
            {
                'src': f'{settings.STATIC_URL}img/pwa-maskable-512.png',
                'sizes': '512x512',
                'type': 'image/png',
                'purpose': 'maskable',
            },
        ],
    }
    return JsonResponse(data, content_type='application/manifest+json')


@require_GET
def service_worker(request):
    response = render(
        request,
        'pwa/sw.js',
        {
            'admin_url': settings.ADMIN_URL.strip('/'),
        },
        content_type='application/javascript; charset=utf-8',
    )
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


@require_GET
@ensure_csrf_cookie
def offline_shell(request):
    return render(request, 'pwa/offline.html')


@require_GET
def offline_catalog_json(request):
    data = build_catalog_snapshot()
    response = JsonResponse(data)
    response['Cache-Control'] = 'public, max-age=300'
    return response


@require_GET
def vapid_key(request):
    return JsonResponse({
        'publicKey': vapid_public_key() if vapid_configured() else '',
        'enabled': vapid_configured(),
    })


def _parse_json(request) -> dict:
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


@require_http_methods(['POST', 'DELETE'])
def push_subscribe(request):
    data = _parse_json(request)
    endpoint = (data.get('endpoint') or '').strip()
    if not endpoint:
        return HttpResponseBadRequest('endpoint required')

    if request.method == 'DELETE':
        PushSubscription.objects.filter(endpoint=endpoint).update(is_active=False)
        return JsonResponse({'ok': True})

    keys = data.get('keys') or {}
    p256dh = (keys.get('p256dh') or '').strip()
    auth = (keys.get('auth') or '').strip()
    if not p256dh or not auth:
        return HttpResponseBadRequest('keys required')

    lang = _normalize_lang(data.get('language') or request.LANGUAGE_CODE)
    if request.user.is_authenticated:
        preferred = getattr(request.user, 'preferred_language', '') or ''
        if preferred:
            lang = _normalize_lang(preferred)
    email = (data.get('email') or '').strip().lower()
    if request.user.is_authenticated and not email:
        email = (getattr(request.user, 'email', '') or '').strip().lower()
    ua = (request.META.get('HTTP_USER_AGENT') or '')[:300]
    defaults = {
        'p256dh': p256dh,
        'auth': auth,
        'language': lang,
        'user_agent': ua,
        'is_active': True,
    }
    if request.user.is_authenticated:
        defaults['user'] = request.user
    if email:
        defaults['email'] = email

    sub, _created = PushSubscription.objects.update_or_create(
        endpoint=endpoint,
        defaults=defaults,
    )
    return JsonResponse({'ok': True, 'id': sub.pk})


@require_POST
def push_bind_email(request):
    data = _parse_json(request)
    endpoint = (data.get('endpoint') or '').strip()
    email = (data.get('email') or '').strip().lower()
    if not endpoint or not email or '@' not in email:
        return HttpResponseBadRequest('endpoint and email required')
    updated = PushSubscription.objects.filter(endpoint=endpoint, is_active=True).update(
        email=email,
        user=request.user if request.user.is_authenticated else None,
    )
    return JsonResponse({'ok': True, 'updated': int(updated)})
