from __future__ import annotations

from django.utils.translation import gettext_lazy as _

HOME_DEFAULTS: dict[tuple[str, str], str] = {
    ('home', 'hero_section_visible'): '1',
    ('home', 'hero_eyebrow'): 'Tobacco Atelier',
    ('home', 'brands_section_visible'): '1',
    ('home', 'catalog_section_visible'): '1',
    ('home', 'catalog_title'): _('Каталог'),
    ('home', 'catalog_all'): _('Увесь каталог'),
    ('home', 'about_section_visible'): '1',
    ('home', 'about_kicker'): _('Історія'),
    ('home', 'about_bg'): '',
    ('home', 'calculator_section_visible'): '1',
    ('home', 'calculator_kicker'): _('Калькулятор'),
    ('home', 'calculator_bg'): '',
    ('home', 'service_section_visible'): '1',
    ('service', 'booking_title'): _('Бронювання'),
    ('service', 'booking_lead'): _(
        'Залиште контакти — менеджер узгодить зручний час візиту.\n\n'
        'Ми передзвонимо протягом робочого дня, щоб підтвердити слот і відповісти на запитання.\n\n'
        'Можна обрати дегустацію, консультацію сомельє або спокійний візит у шоурум — '
        'підлаштуємось під ваш ритм.'
    ),
    ('service', 'booking_cta'): _('Обрати час'),
    ('service', 'booking_image'): '',
    ('service', 'b2b_title'): 'B2B',
    ('service', 'b2b_lead'): _('Прайс для барів, готелів і корпоративних подарунків.'),
    ('service', 'b2b_cta'): _('Запросити прайс'),
    ('service', 'b2b_image'): '',
}

HOME_LABELS: dict[tuple[str, str], str] = {
    ('home', 'hero_section_visible'): 'Показувати головний банер',
    ('home', 'hero_eyebrow'): 'Мітка над заголовком',
    ('home', 'brands_section_visible'): 'Показувати бренди',
    ('home', 'catalog_section_visible'): 'Показувати каталог',
    ('home', 'catalog_title'): 'Заголовок каталогу',
    ('home', 'catalog_all'): 'Посилання «Увесь каталог»',
    ('home', 'about_section_visible'): 'Показувати історію',
    ('home', 'about_kicker'): 'Мітка секції історії',
    ('home', 'about_bg'): 'Фонове фото блоку історії',
    ('home', 'calculator_section_visible'): 'Показувати калькулятор',
    ('home', 'calculator_kicker'): 'Мітка калькулятора',
    ('home', 'calculator_bg'): 'Фон калькулятора',
    ('home', 'service_section_visible'): 'Показувати сервіс',
    ('service', 'booking_title'): 'Бронювання — заголовок',
    ('service', 'booking_lead'): 'Бронювання — текст',
    ('service', 'booking_cta'): 'Бронювання — кнопка',
    ('service', 'booking_image'): 'Бронювання — фото',
    ('service', 'b2b_title'): 'B2B — заголовок',
    ('service', 'b2b_lead'): 'B2B — текст',
    ('service', 'b2b_cta'): 'B2B — кнопка',
    ('service', 'b2b_image'): 'B2B — фото',
}

HOME_TYPES: dict[tuple[str, str], str] = {
    ('home', 'about_bg'): 'image',
    ('home', 'calculator_bg'): 'image',
    ('service', 'booking_image'): 'image',
    ('service', 'b2b_image'): 'image',
}

HOME_INLINE = {
    'hero_eyebrow', 'catalog_title', 'catalog_all', 'about_kicker',
    'calculator_kicker', 'booking_title', 'booking_cta', 'b2b_title', 'b2b_cta',
}
HOME_MULTILINE = {'booking_lead', 'b2b_lead'}
