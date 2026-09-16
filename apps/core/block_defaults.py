from __future__ import annotations

from apps.core.block_defaults_home import (
    HOME_DEFAULTS,
    HOME_INLINE,
    HOME_LABELS,
    HOME_MULTILINE,
    HOME_TYPES,
)
from apps.core.block_defaults_pages import (
    PAGE_DEFAULTS,
    PAGE_INLINE,
    PAGE_LABELS,
    PAGE_MULTILINE,
    PAGE_TYPES,
)

BLOCK_DEFAULTS: dict[tuple[str, str], str] = {**HOME_DEFAULTS, **PAGE_DEFAULTS}

BLOCK_FIELD_LABELS: dict[tuple[str, str], str] = {
    key: key[1].replace('_', ' ') for key in BLOCK_DEFAULTS
}
BLOCK_FIELD_LABELS.update(HOME_LABELS)
BLOCK_FIELD_LABELS.update(PAGE_LABELS)

BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {
    key: 'text' for key in BLOCK_DEFAULTS
}
BLOCK_CONTENT_TYPES.update(HOME_TYPES)
BLOCK_CONTENT_TYPES.update(PAGE_TYPES)

INLINE_KEYS = HOME_INLINE | PAGE_INLINE
MULTILINE_KEYS = HOME_MULTILINE | PAGE_MULTILINE

HISTORY_IMAGE_FALLBACKS: tuple[str, ...] = (
    'img/history/01-intro.jpg',
    'img/history/02-origins.jpg',
    'img/history/03-golden.jpg',
    'img/history/04-today.jpg',
)

BRAND_IMAGE_FALLBACKS: dict[str, str] = {
    'aj-fernandez': 'img/brands/01-aj.jpg',
    'oliva': 'img/brands/02-oliva.jpg',
    'perdomo': 'img/brands/03-perdomo.jpg',
    'casa-turrent': 'img/brands/04-turrent.jpg',
}

BRAND_CARD_TEXT_DEFAULTS: dict[str, str] = {
    'aj-fernandez': (
        'Нікарагуанська школа майстерності: насичений смак, щільна скрутка '
        'та характерний maduro. Сигари AJ Fernandez — для тих, хто цінує '
        'глибину профілю, довгий фініш і ритуал повільного куріння.'
    ),
    'oliva': (
        'Глибокі профілі з нотами какао, шкіри та кедру — Oliva створює '
        'сигари для довгого вечірнього ритуалу. Баланс сили й елегантності, '
        'витриманий тютюн і бездоганна скрутка.'
    ),
    'perdomo': (
        'Свіжі ноти тютюнового листа, акуратна ферментація та чистий фініш. '
        'Perdomo — сімейна традиція, де кожна сигара проходить відбір '
        'і контроль вологості для ідеального куріння.'
    ),
    'casa-turrent': (
        'Земляні тони мексиканського terroir, деревʼяна коробка та аксесуари '
        'для повільного ритуалу. Casa Turrent поєднує історію родини '
        'з сучасним характером преміальної сигари.'
    ),
}

PAGE_BG_IMAGE_FALLBACKS: dict[tuple[str, str], str] = {
    ('faq', 'bg'): 'img/calculator/lounge-bg.jpg',
    ('delivery', 'bg'): 'img/calculator/lounge-bg.jpg',
    ('home', 'calculator_bg'): 'img/calculator/lounge-bg.jpg',
    ('home', 'about_bg'): 'img/history/bg.jpg',
    ('service', 'booking_image'): 'img/booking/lounge.jpg',
    ('service', 'b2b_image'): 'img/service/b2b.jpg',
}

HISTORY_SLIDE_DEFAULTS: tuple[dict[str, str | int], ...] = (
    {
        'year_label': 'Intro',
        'title': 'Про Royal Smoke',
        'text': (
            'Сигара — це повільний ритуал: від древніх обрядів до майстрів скрутки. '
            'У Royal Smoke ми бережемо цей темп — добірний лист, тиша хумідора '
            'і дим, вартуючий уваги.'
        ),
        'image_static': 'img/history/01-intro.jpg',
        'cta_label': '',
        'cta_url': '',
        'sort_order': 0,
    },
    {
        'year_label': '1492+',
        'title': 'Карибські витоки',
        'text': (
            'У Карибах дим був мовою зустрічі й обряду, а не розвагою. '
            'Саме тут народжується шлях сигари — від живого листа до ритуалу часу.'
        ),
        'image_static': 'img/history/02-origins.jpg',
        'cta_label': '',
        'cta_url': '',
        'sort_order': 1,
    },
    {
        'year_label': 'XIX ст.',
        'title': 'Золота доба',
        'text': (
            'Куба XIX століття задає канон: вітола, дисципліна скрутки, імена легенд. '
            'Сигара стає мовою смаку й статусу — витонченою й безкомпромісною.'
        ),
        'image_static': 'img/history/03-golden.jpg',
        'cta_label': '',
        'cta_url': '',
        'sort_order': 2,
    },
    {
        'year_label': 'Сьогодні',
        'title': 'Новий світ',
        'text': (
            'Смак уже не має однієї адреси: Нікарагуа, Домінікана, Гондурас. '
            'Ми обираємо мануфактури за характером диму — тихо, точно, без зайвого шуму.'
        ),
        'image_static': 'img/history/04-today.jpg',
        'cta_label': '',
        'cta_url': '',
        'sort_order': 3,
    },
)

FAQ_ITEM_DEFAULTS: tuple[dict[str, str], ...] = (
    {
        'question': 'Як зберігати сигари?',
        'answer': 'У хумідорі при 68–72% вологості та 16–20°C. Ми відправляємо в термобоксі.',
    },
    {
        'question': 'Чи потрібна реєстрація для покупки?',
        'answer': 'Ні, гостьове оформлення доступне. Кабінет зручний для повторних замовлень.',
    },
    {
        'question': 'Які терміни доставки?',
        'answer': 'Київ — часто того ж дня, Україна — 1–2 дні. Деталі на сторінці «Доставка і оплата».',
    },
    {
        'question': 'Чи можна повернути товар?',
        'answer': 'Тютюнові вироби належної якості не підлягають поверненню. Брак розглядаємо індивідуально.',
    },
    {
        'question': 'Як працює бронювання?',
        'answer': (
            'Залиште імʼя та телефон у блоці «Бронювання» на головній — '
            'менеджер узгодить зручний час візиту.'
        ),
    },
)

LEGAL_DOC_DEFAULTS: tuple[dict[str, str], ...] = (
    {
        'slug': 'privacy',
        'title': 'Політика конфіденційності',
        'body': (
            '<p>Ми обробляємо персональні дані (імʼя, телефон, email, адресу доставки) '
            'лише для виконання замовлень і зворотного звʼязку. Дані не продаємо третім сторонам.</p>'
        ),
    },
    {
        'slug': 'terms',
        'title': 'Умови користування',
        'body': (
            '<p>Сайт Royal Smoke пропонує тютюнові вироби та аксесуари повнолітнім відвідувачам. '
            'Оформлюючи замовлення, ви підтверджуєте вік 21+ та згоду з умовами продажу.</p>'
        ),
    },
    {
        'slug': 'age',
        'title': 'Вікова політика',
        'body': (
            '<p>Доступ до вітрини можливий лише після підтвердження віку (cookie age_ok). '
            'Особам молодше 21 року продаж заборонено.</p>'
        ),
    },
    {
        'slug': 'cookies',
        'title': 'Файли cookie',
        'body': (
            '<p>Використовуємо необхідні cookies для сесії кошика, age gate та мови. '
            'Аналітичні cookies — лише за згодою, якщо увімкнено на проєкті.</p>'
        ),
    },
)


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible') or key.endswith('_section_visible')
