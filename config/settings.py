"""Django settings — Royal Smoke."""

from __future__ import annotations

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _env_bool(key: str, default: bool) -> bool:
    raw = os.environ.get(key)
    if raw is None or raw == '':
        return default
    return raw.lower() in ('1', 'true', 'yes')


SECRET_KEY = os.environ.get('SECRET_KEY', 'insecure-dev-key')
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('1', 'true', 'yes')
_INSECURE_SECRET_KEYS = {
    '',
    'insecure-dev-key',
    'change-me-in-production',
    'generate-a-long-random-string',
}
if not DEBUG and SECRET_KEY in _INSECURE_SECRET_KEYS:
    raise ImproperlyConfigured('SECRET_KEY must be set when DEBUG=False')
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,testserver').split(',')
    if h.strip()
]

_ADMIN_SLUG = (os.environ.get('ADMIN_URL') or 'rs-admin').strip().strip('/')
ADMIN_URL = f'{_ADMIN_SLUG}/'

INSTALLED_APPS = [
    'modeltranslation',
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django_htmx',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'csp',
    'apps.accounts',
    'apps.core',
    'apps.catalog',
    'apps.cart',
    'apps.orders',
    'apps.booking',
    'apps.calculator',
    'apps.leads',
    'apps.pages',
    'apps.api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'csp.middleware.CSPMiddleware',
    'apps.core.middleware.AgeGateMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_globals',
                'apps.cart.context_processors.cart_context',
                'apps.accounts.context_processors.wishlist_context',
                'apps.catalog.context_processors.compare_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

_DB_URL = os.environ.get(
    'DATABASE_URL',
    'postgres://olegbonislavskyi@localhost:5432/royalsmoke',
)
# Simple postgres://user@host:port/db parser (no password for local peer/trust).
if _DB_URL.startswith('postgres'):
    from urllib.parse import urlparse

    _u = urlparse(_DB_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': (_u.path or '/royalsmoke').lstrip('/') or 'royalsmoke',
            'USER': _u.username or '',
            'PASSWORD': _u.password or '',
            'HOST': _u.hostname or 'localhost',
            'PORT': str(_u.port or 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'apps.core.validation.password.StrongPasswordValidator'},
]

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:cabinet'
LOGOUT_REDIRECT_URL = 'pages:home'

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'uk')
TIME_ZONE = os.environ.get('TIME_ZONE', 'Europe/Kyiv')
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('uk', 'Українська'),
    ('en', 'English'),
    ('zh-hans', '中文'),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uk'
MODELTRANSLATION_LANGUAGES = ('uk', 'en', 'zh-hans')
LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': (
            'django.contrib.staticfiles.storage.StaticFilesStorage'
            if DEBUG
            else 'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CURRENCY_CODE = 'UAH'
CURRENCY_SYMBOL = '₴'
DEFAULT_MARKET = 'UA'
AGE_GATE_COOKIE = 'age_ok'
AGE_GATE_DAYS = 30

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 24,
    'DEFAULT_THROTTLE_RATES': {
        'anon_checkout': '20/hour',
    },
}

from csp.constants import NONCE, SELF  # noqa: E402

CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': [SELF],
        'script-src': [SELF, NONCE, 'https://unpkg.com'],
        'style-src': [SELF, 'https://fonts.googleapis.com', "'unsafe-inline'"],
        'font-src': [SELF, 'https://fonts.gstatic.com'],
        'img-src': [SELF, 'data:', 'blob:', 'https:'],
        'connect-src': [SELF],
        'frame-ancestors': [SELF],
    }
}

EMAIL_HOST = os.environ.get('EMAIL_HOST', '').strip()
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587') or 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('1', 'true', 'yes')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@royalsmoke.ua')
NOTIFY_EMAIL = os.environ.get('NOTIFY_EMAIL', 'admin@royalsmoke.ua')
if EMAIL_HOST:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

LIQPAY_PUBLIC_KEY = os.environ.get('LIQPAY_PUBLIC_KEY', '')
LIQPAY_PRIVATE_KEY = os.environ.get('LIQPAY_PRIVATE_KEY', '')
LIQPAY_SANDBOX = os.environ.get('LIQPAY_SANDBOX', '1').lower() in ('1', 'true', 'yes')
# Test checkout without LiqPay keys. Keep off in production.
DEMO_PAYMENTS = _env_bool('DEMO_PAYMENTS', DEBUG)

NOVA_POSHTA_API_KEY = os.environ.get('NOVA_POSHTA_API_KEY', '')
NP_SENDER_CITY_REF = os.environ.get('NP_SENDER_CITY_REF', '')
NP_SENDER_WAREHOUSE_REF = os.environ.get('NP_SENDER_WAREHOUSE_REF', '')
NP_SENDER_CONTACT = os.environ.get('NP_SENDER_CONTACT', '')
NP_SENDER_PHONE = os.environ.get('NP_SENDER_PHONE', '')
NP_SENDER_REF = os.environ.get('NP_SENDER_REF', '')
NP_CONTACT_SENDER = os.environ.get('NP_CONTACT_SENDER', '')
NP_SENDER_COUNTERPARTY_REF = os.environ.get('NP_SENDER_COUNTERPARTY_REF', '')

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
if DEBUG:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
else:
    SECURE_SSL_REDIRECT = _env_bool('SECURE_SSL_REDIRECT', False)
    SESSION_COOKIE_SECURE = _env_bool('SESSION_COOKIE_SECURE', False)
    CSRF_COOKIE_SECURE = _env_bool('CSRF_COOKIE_SECURE', False)
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0') or 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0

UNFOLD = {
    'SITE_TITLE': 'Royal Smoke',
    'SITE_HEADER': 'Royal Smoke Admin',
    'SITE_SYMBOL': 'smoking_rooms',
    'SHOW_HISTORY': True,
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': True,
        'navigation': [],  # filled in apps.core.admin_nav
    },
}

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000,http://localhost:8000').split(',')
    if o.strip()
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'apps': {'handlers': ['console'], 'level': 'INFO'},
        'apps.orders.services': {'handlers': ['console'], 'level': 'INFO'},
        'apps.core.services': {'handlers': ['console'], 'level': 'INFO'},
    },
}
