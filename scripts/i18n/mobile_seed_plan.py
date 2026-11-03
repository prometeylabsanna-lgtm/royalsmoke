"""Які фрази M001–M159 лягають у моделі мобільного застосунку."""

from __future__ import annotations

from mobile_tables import Phrase

# Поле моделі → максимальна довжина. TextField не обмежені.
CHAR_LIMITS: dict[str, int] = {
    'kicker': 120,
    'title': 255,
    'subtitle': 255,
    'cta_primary': 120,
    'cta_secondary': 120,
    'confirm_label': 120,
    'success_title': 255,
    'contact_address': 255,
    'contact_hours': 255,
    'contact_phone': 64,
    'app_version': 64,
    'country': 80,
    'name': 160,
    'short_name': 80,
    'mono': 8,
    'label': 120,
    'value': 255,
    'index_label': 8,
    'line_name': 160,
    'legal_title': 255,
}

SCREENS: dict[str, dict[str, str]] = {
    'splash': {'kicker': 'M001', 'title': 'M002', 'cta_primary': 'M003'},
    'age': {
        'kicker': 'M004',
        'title': 'M005',
        'subtitle': 'M006',
        'body': 'M007',
        'legal_note': 'M010',
        'confirm_label': 'M009',
        'cta_secondary': 'M008',
    },
    'home': {
        'kicker': 'M011',
        'title': 'M012',
        'body': 'M013',
        'cta_primary': 'M014',
        'cta_secondary': 'M015',
    },
    'house': {
        'kicker': 'M016',
        'title': 'M017',
        'body': 'M018',
        'cta_primary': 'M019',
        'cta_secondary': 'M020',
    },
    'visit': {
        'kicker': 'M030',
        'title': 'M028',
        'cta_primary': 'M032',
        'success_title': 'M033',
        'success_body': 'M034',
        'body_secondary': 'M031',
    },
}

HOUSE_BLOCKS: tuple[tuple[str, str, str], ...] = (
    ('M021', 'M022', 'M023'),
    ('M024', 'M025', 'M026'),
    ('M027', 'M028', 'M029'),
)

SETTINGS = {
    'app_version': 'M035',
    'app_blurb': 'M036',
    'contact_address': 'M037',
    'contact_phone': 'M038',
    'contact_hours': 'M039',
}

LEGAL: dict[str, dict[str, object]] = {
    'privacy': {'title': 'M090', 'body': ['M091', 'M092', 'M093', 'M094', 'M095']},
    'terms': {'title': 'M096', 'body': ['M097', 'M098', 'M099', 'M100', 'M101']},
    'age': {'title': 'M102', 'body': ['M103', 'M104', 'M105', 'M106', 'M107']},
    'about': {'title': 'M108', 'body': ['M109', 'M110', 'M111', 'M112', 'M113']},
}

BRANDS: tuple[dict, ...] = (
    {
        'slug': 'aj',
        'panel': 'amber',
        'cover': 'brands/aj.jpg',
        'name': 'M040',
        'short_name': 'M041',
        'mono': 'M041',
        'country': 'M042',
        'heritage': 'M043',
        'facts': (('M044', 'M045'), ('M046', 'M047'), ('M048', 'M049'), ('M050', 'M051')),
        'lines': ('M052', 'M053', 'M054', 'M055'),
    },
    {
        'slug': 'oliva',
        'panel': 'burgundy',
        'cover': 'brands/oliva.jpg',
        'name': 'M056',
        'short_name': 'M056',
        'mono': 'M057',
        'country': 'M042',
        'heritage': 'M058',
        'facts': (('M044', 'M045'), ('M059', 'M060'), ('M061', 'M062'), ('M050', 'M063')),
        'lines': ('M064', 'M065', 'M066', 'M067'),
    },
    {
        'slug': 'perdomo',
        'panel': 'green',
        'cover': 'brands/perdomo.jpg',
        'name': 'M068',
        'short_name': 'M068',
        'mono': 'M069',
        'country': 'M042',
        'heritage': 'M070',
        'facts': (('M044', 'M045'), ('M046', 'M071'), ('M072', 'M073'), ('M074', 'M075')),
        'lines': ('M076', 'M077', 'M078'),
    },
    {
        'slug': 'turrent',
        'panel': 'brown',
        'cover': 'brands/turrent.jpg',
        'name': 'M079',
        'short_name': 'M079',
        'mono': 'M080',
        'country': 'M081',
        'heritage': 'M082',
        'facts': (('M044', 'M083'), ('M048', 'M084'), ('M050', 'M085')),
        'lines': ('M086', 'M087', 'M088', 'M089'),
    },
)

HERO = {'home': 'home/hero.jpg', 'house': 'home/house.jpg'}

# Поля, які реально перекладаються (решта — вордмарк / номер / телефон).
TRANSLATED_SETTINGS = ('app_blurb', 'contact_address', 'contact_hours')
TRANSLATED_BRAND = ('country', 'heritage')
TRANSLATED_FACT = ('label', 'value')
TRANSLATED_SCREEN = (
    'kicker', 'title', 'subtitle', 'body', 'body_secondary',
    'cta_primary', 'cta_secondary', 'confirm_label', 'legal_note',
    'success_title', 'success_body',
)
TRANSLATED_BLOCK = ('title', 'body')
TRANSLATED_LEGAL = ('title', 'body')


def _check(mid: str, field: str, value: str, errors: list[str]) -> None:
    limit = CHAR_LIMITS.get(field)
    if limit is not None and len(value) > limit:
        errors.append(f'{mid} {field}: {len(value)} > {limit}')


def check_lengths(rows: dict[str, Phrase]) -> list[str]:
    errors: list[str] = []
    for spec in SCREENS.values():
        for field, mid in spec.items():
            for lang in rows[mid].texts:
                _check(mid, field, rows[mid].text(lang), errors)
    for index_id, title_id, body_id in HOUSE_BLOCKS:
        for lang in rows[index_id].texts:
            _check(index_id, 'index_label', rows[index_id].text(lang), errors)
            _check(title_id, 'title', rows[title_id].text(lang), errors)
    for field, mid in SETTINGS.items():
        for lang in rows[mid].texts:
            _check(mid, field, rows[mid].text(lang), errors)
    for spec in BRANDS:
        for field in ('name', 'short_name', 'mono', 'country'):
            mid = spec[field]
            for lang in rows[mid].texts:
                _check(mid, field, rows[mid].text(lang), errors)
        for label_id, value_id in spec['facts']:
            for lang in rows[label_id].texts:
                _check(label_id, 'label', rows[label_id].text(lang), errors)
                _check(value_id, 'value', rows[value_id].text(lang), errors)
        for mid in spec['lines']:
            for lang in rows[mid].texts:
                _check(mid, 'line_name', rows[mid].text(lang), errors)
    for spec in LEGAL.values():
        mid = spec['title']
        for lang in rows[mid].texts:
            _check(mid, 'legal_title', rows[mid].text(lang), errors)
    return errors
