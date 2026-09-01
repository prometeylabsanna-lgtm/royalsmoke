from __future__ import annotations

BLOCK_DEFAULTS: dict[tuple[str, str], str] = {
    ('home', 'hero_section_visible'): '1',
    ('home', 'hero_eyebrow'): 'Tobacco Atelier',
    ('home', 'categories_section_visible'): '1',
    ('home', 'categories_title'): 'Ключові категорії',
    ('home', 'top_section_visible'): '1',
    ('home', 'top_title'): 'Топ продажів',
    ('home', 'new_section_visible'): '1',
    ('home', 'new_title'): 'Новинки',
    ('home', 'about_section_visible'): '1',
    ('home', 'about_kicker'): 'Історія',
    ('home', 'about_bg'): '',
    ('home', 'service_section_visible'): '1',
    ('home', 'service_kicker'): 'Сервіс',
    ('site', 'header_search_placeholder'): 'Пошук сигар, брендів, аксесуарів…',
    ('site', 'footer_tagline'): 'Сигари, відібрані вручну для тих, хто знає різницю.',
    ('service', 'booking_title'): 'Бронювання',
    ('service', 'booking_lead'): 'Залиште контакти — менеджер узгодить зручний час візиту.',
    ('service', 'calculator_title'): 'Калькулятор підбору',
    ('service', 'calculator_lead'): 'Чотири кроки — три рекомендації з поясненням.',
    ('service', 'b2b_title'): 'B2B',
    ('service', 'b2b_lead'): 'Прайс і умови для барів, готелів і корпоративних подарунків.',
    ('service', 'delivery_title'): 'Доставка',
    ('service', 'delivery_lead'): 'Київ — того ж дня, Україна — 1–2 дні. Термобокси для сигар.',
}

BLOCK_FIELD_LABELS: dict[tuple[str, str], str] = {
    key: key[1].replace('_', ' ').capitalize() for key in BLOCK_DEFAULTS
}
BLOCK_FIELD_LABELS.update({
    ('home', 'hero_section_visible'): 'Показувати Hero',
    ('home', 'hero_eyebrow'): 'Мітка над заголовком',
    ('home', 'categories_title'): 'Заголовок категорій',
    ('home', 'top_title'): 'Заголовок топу',
    ('home', 'new_title'): 'Заголовок новинок',
    ('home', 'about_kicker'): 'Мітка секції історії',
    ('home', 'about_bg'): 'Фонове фото блоку історії',
    ('site', 'header_search_placeholder'): 'Placeholder пошуку',
    ('site', 'footer_tagline'): 'Слоган у футері',
})

BLOCK_CONTENT_TYPES: dict[tuple[str, str], str] = {
    key: 'text' for key in BLOCK_DEFAULTS
}
BLOCK_CONTENT_TYPES[('home', 'about_bg')] = 'image'

INLINE_KEYS = {
    'hero_eyebrow', 'categories_title', 'top_title', 'new_title', 'about_kicker',
    'service_kicker', 'header_search_placeholder', 'footer_tagline',
    'booking_title', 'calculator_title', 'b2b_title', 'delivery_title',
}
MULTILINE_KEYS = {
    'booking_lead', 'calculator_lead', 'b2b_lead', 'delivery_lead',
}

HISTORY_IMAGE_FALLBACKS: tuple[str, ...] = (
    'img/history/01-intro.jpg',
    'img/history/02-origins.jpg',
    'img/history/03-golden.jpg',
    'img/history/04-today.jpg',
)

HISTORY_SLIDE_DEFAULTS: tuple[dict[str, str | int], ...] = (
    {
        'year_label': 'Intro',
        'title': 'Про Royal Smoke',
        'text': (
            'Від майя та таїно до кубинських фабрик і сучасних мануфактур — '
            'сигара як ритуал часу, який ми зберігаємо в Royal Smoke.\n\n'
            'У Royal Smoke ми зберігаємо цей спадок: відбір листів, правильний клімат '
            'хумідора і повільний дим як частина культури.'
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
            'Перші згадки про скручений тютюн у Карибах зʼявляються разом із зустріччю '
            'європейців і народів таїно. Дим тоді був не розвагою, а частиною обряду, '
            'мови та спільноти.\n\n'
            'Саме звідси починається шлях сигари: від листа до ритуалу, від вогню до '
            'повільного часу — того самого, який ми досі шукаємо в кожній вітолі.'
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
            'У XIX столітті кубинські фабрики формують канон: сорти, вітоли, '
            'дисципліна скрутки і культура бренду. Зʼявляються імена, які досі '
            'задають міру смаку й престижу.\n\n'
            'Тоді сигара остаточно стає мовою еліти й ремесла водночас — баланс '
            'міцності, аромату й форми, який ми читаємо в класичних лініях і сьогодні.'
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
            'Сьогодні карта смаку ширша за одну країну: Нікарагуа, Домінікана, '
            'Гондурас — регіони, де ростуть нові легенди й лімітовані лінії.\n\n'
            'У Royal Smoke ми відбираємо ці мануфактури вручну: не за шумом назви, '
            'а за характером диму, стабільністю партій і тим, чи варта сигара '
            'повільного вечора.'
        ),
        'image_static': 'img/history/04-today.jpg',
        'cta_label': '',
        'cta_url': '',
        'sort_order': 3,
    },
)


def is_visibility_key(key: str) -> bool:
    return key.endswith('_visible') or key.endswith('_section_visible')
