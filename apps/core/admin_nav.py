from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.core.site_content_sections import CONTENT_SECTIONS

SIDEBAR_GROUPS: tuple[tuple[str, str, bool], ...] = (
    ('home', _('Головна'), False),
    ('catalog', _('Каталог'), True),
    ('about', _('Про нас'), True),
    ('blog', _('Блог'), True),
    ('faq', _('FAQ'), True),
    ('contact', _('Контакти'), True),
    ('delivery', _('Доставка і оплата'), True),
    ('b2b', _('B2B'), True),
    ('booking', _('Бронювання'), True),
    ('cart', _('Кошик'), True),
    ('checkout', _('Оформлення'), True),
    ('cabinet', _('Кабінет'), True),
    ('age', _('Вікова перевірка'), True),
    ('chrome', _('Шапка і футер'), True),
)


def _cms_items_for(group_key: str) -> list[dict]:
    items = []
    for section in CONTENT_SECTIONS:
        if section.sidebar_group != group_key or not section.admin_model_name:
            continue
        items.append({
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:core_{section.admin_model_name}_changelist'),
        })
    if group_key == 'faq':
        items.append({
            'title': _('Питання'),
            'icon': 'quiz',
            'link': reverse_lazy('admin:pages_faqitem_changelist'),
        })
    if group_key == 'blog':
        items.append({
            'title': _('Статті'),
            'icon': 'newspaper',
            'link': reverse_lazy('admin:pages_blogpost_changelist'),
        })
    if group_key == 'about':
        pass
    return items


def build_unfold_navigation() -> list[dict]:
    nav: list[dict] = []
    for key, title, separator in SIDEBAR_GROUPS:
        items = _cms_items_for(key)
        if not items:
            continue
        nav.append({
            'title': title,
            'separator': separator,
            'collapsible': True,
            'items': items,
        })

    nav.append({
        'title': _('Документи'),
        'separator': True,
        'collapsible': True,
        'items': [
            {
                'title': _('Юридичні документи'),
                'icon': 'gavel',
                'link': reverse_lazy('admin:pages_legaldocument_changelist'),
            },
        ],
    })
    nav.append({
        'title': _('Каталог товарів'),
        'separator': True,
        'collapsible': True,
        'items': [
            {'title': _('Товари'), 'icon': 'inventory_2', 'link': reverse_lazy('admin:catalog_product_changelist')},
            {'title': _('Категорії'), 'icon': 'category', 'link': reverse_lazy('admin:catalog_category_changelist')},
            {'title': _('Бренди'), 'icon': 'storefront', 'link': reverse_lazy('admin:catalog_brand_changelist')},
            {'title': _('Лінії'), 'icon': 'view_week', 'link': reverse_lazy('admin:catalog_productline_changelist')},
            {'title': _('Теги'), 'icon': 'sell', 'link': reverse_lazy('admin:catalog_tag_changelist')},
        ],
    })
    nav.append({
        'title': _('Продажі'),
        'separator': True,
        'collapsible': True,
        'items': [
            {'title': _('Замовлення'), 'icon': 'shopping_bag', 'link': reverse_lazy('admin:orders_order_changelist')},
            {'title': _('Ліди'), 'icon': 'support_agent', 'link': reverse_lazy('admin:leads_lead_changelist')},
            {'title': _('Бронювання'), 'icon': 'event', 'link': reverse_lazy('admin:booking_booking_changelist')},
            {'title': _('Калькулятор'), 'icon': 'calculate', 'link': reverse_lazy('admin:calculator_calculatorquestion_changelist')},
        ],
    })
    nav.append({
        'title': _('Користувачі'),
        'separator': True,
        'collapsible': True,
        'items': [
            {'title': _('Акаунти'), 'icon': 'person', 'link': reverse_lazy('admin:accounts_user_changelist')},
            {'title': _('Налаштування сайту'), 'icon': 'settings', 'link': reverse_lazy('admin:core_sitesettings_changelist')},
        ],
    })
    return nav
