"""Блоки юридичних сторінок (privacy / terms / age_policy / cookies)."""

from __future__ import annotations

from django.utils.translation import gettext_lazy as _

from apps.core.legal_privacy_body import PRIVACY_BODY_UK

LEGAL_DEFAULTS: dict[tuple[str, str], str] = {
    ('privacy', 'title'): _('Політика конфіденційності'),
    ('privacy', 'lead'): _('Як ми збираємо, зберігаємо та захищаємо ваші дані.'),
    ('privacy', 'bg'): '',
    ('privacy', 'body'): PRIVACY_BODY_UK,
    ('terms', 'title'): _('Умови користування'),
    ('terms', 'lead'): _('Правила користування сайтом і умови продажу.'),
    ('terms', 'bg'): '',
    ('terms', 'body'): (
        '<p>Сайт Royal Smoke пропонує тютюнові вироби та аксесуари повнолітнім відвідувачам. '
        'Оформлюючи замовлення, ви підтверджуєте вік 21+ та згоду з умовами продажу.</p>'
    ),
    ('age_policy', 'title'): _('Вікова політика'),
    ('age_policy', 'lead'): _('Доступ лише для повнолітніх відвідувачів 21+.'),
    ('age_policy', 'bg'): '',
    ('age_policy', 'body'): (
        '<p>Доступ до вітрини можливий лише після підтвердження віку (cookie age_ok). '
        'Особам молодше 21 року продаж заборонено.</p>'
    ),
    ('cookies', 'title'): _('Файли cookie'),
    ('cookies', 'lead'): _('Які cookies використовує сайт і навіщо.'),
    ('cookies', 'bg'): '',
    ('cookies', 'body'): (
        '<p>Використовуємо необхідні cookies для сесії кошика, age gate та мови. '
        'Аналітичні cookies — лише за згодою, якщо увімкнено на проєкті.</p>'
    ),
}

LEGAL_LABELS: dict[tuple[str, str], str] = {
    ('privacy', 'title'): 'Заголовок',
    ('privacy', 'lead'): 'Лід',
    ('privacy', 'bg'): 'Фон сторінки',
    ('privacy', 'body'): 'Текст політики',
    ('terms', 'title'): 'Заголовок',
    ('terms', 'lead'): 'Лід',
    ('terms', 'bg'): 'Фон сторінки',
    ('terms', 'body'): 'Текст умов',
    ('age_policy', 'title'): 'Заголовок',
    ('age_policy', 'lead'): 'Лід',
    ('age_policy', 'bg'): 'Фон сторінки',
    ('age_policy', 'body'): 'Текст політики',
    ('cookies', 'title'): 'Заголовок',
    ('cookies', 'lead'): 'Лід',
    ('cookies', 'bg'): 'Фон сторінки',
    ('cookies', 'body'): 'Текст про cookies',
}

LEGAL_TYPES: dict[tuple[str, str], str] = {
    ('privacy', 'bg'): 'image',
    ('terms', 'bg'): 'image',
    ('age_policy', 'bg'): 'image',
    ('cookies', 'bg'): 'image',
}

LEGAL_INLINE = {
    'title',
}
LEGAL_MULTILINE = {
    'lead',
    'body',
}
