"""Мови вітрини Royal Smoke — єдине джерело для settings, тестів і скриптів.

Адмінка лишається українською; мови нижче стосуються лише публічної вітрини.
Нову мову додаємо тут: рядок у STOREFRONT_LANGUAGES, валюта в LANGUAGE_CURRENCY,
fallback у MODELTRANSLATION_FALLBACK_LANGUAGES і курс у адмінці «Курси валют».
"""

from __future__ import annotations

import django.conf.locale

STOREFRONT_LANGUAGES: list[tuple[str, str]] = [
    ('uk', 'Українська'),
    ('en', 'English'),
    ('zh-hans', '中文'),
    ('ms', 'Bahasa Melayu'),
    ('fil', 'Filipino'),
    ('id', 'Bahasa Indonesia'),
    ('vi', 'Tiếng Việt'),
]

# Мови, які бачить відвідувач у перемикачі. Порядок — порядок пунктів у списку.
STOREFRONT_LANGUAGES_VISIBLE: tuple[str, ...] = (
    'uk', 'en', 'zh-hans', 'ms', 'fil', 'id', 'vi',
)

# Короткі підписи в перемикачі мов.
LANGUAGE_SHORT_LABELS: dict[str, str] = {
    'uk': 'UA',
    'en': 'EN',
    'zh-hans': 'CN',
    'ms': 'MS',
    'fil': 'FIL',
    'id': 'ID',
    'vi': 'VI',
}

MODELTRANSLATION_LANGUAGE_CODES: tuple[str, ...] = tuple(
    code for code, _name in STOREFRONT_LANGUAGES
)

# Порожнє поле нової мови: спочатку англійська, потім українська (як і раніше для en/zh).
MODELTRANSLATION_FALLBACK: dict[str, tuple[str, ...]] = {
    'default': ('uk',),
    'ms': ('en', 'uk'),
    'fil': ('en', 'uk'),
    'id': ('en', 'uk'),
    'vi': ('en', 'uk'),
}

# Мова вітрини → ISO 4217. Курс гривні для кожної валюти — в адмінці «Курси валют».
LANGUAGE_CURRENCY: dict[str, str] = {
    'uk': 'UAH',
    'en': 'USD',
    'zh-hans': 'CNY',
    'ms': 'MYR',
    'fil': 'PHP',
    'id': 'IDR',
    'vi': 'VND',
}

# Django не знає Filipino: без цього запису {% get_language_info %}, перемикач мов і
# check_for_language() для префікса /fil/ не працюють.
EXTRA_LANG_INFO: dict[str, dict] = {
    'fil': {
        'bidi': False,
        'code': 'fil',
        'name': 'Filipino',
        'name_local': 'Filipino',
    },
}
django.conf.locale.LANG_INFO = dict(django.conf.locale.LANG_INFO, **EXTRA_LANG_INFO)
