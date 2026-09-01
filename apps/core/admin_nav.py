from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.core.site_content_registry import CONTENT_SECTIONS


def build_unfold_navigation() -> list[dict]:
    content_items = []
    for section in CONTENT_SECTIONS:
        if not section.admin_model_name:
            continue
        content_items.append({
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': reverse_lazy(f'admin:core_{section.admin_model_name}_changelist'),
        })

    return [
        {
            'title': _('Вміст сторінок'),
            'separator': True,
            'items': content_items,
        },
        {
            'title': _('Каталог'),
            'separator': True,
            'items': [
                {'title': _('Товари'), 'icon': 'inventory_2', 'link': reverse_lazy('admin:catalog_product_changelist')},
                {'title': _('Категорії'), 'icon': 'category', 'link': reverse_lazy('admin:catalog_category_changelist')},
                {'title': _('Бренди'), 'icon': 'storefront', 'link': reverse_lazy('admin:catalog_brand_changelist')},
                {'title': _('Лінії'), 'icon': 'view_week', 'link': reverse_lazy('admin:catalog_productline_changelist')},
                {'title': _('Теги'), 'icon': 'sell', 'link': reverse_lazy('admin:catalog_tag_changelist')},
            ],
        },
        {
            'title': _('Продажі'),
            'separator': True,
            'items': [
                {'title': _('Замовлення'), 'icon': 'shopping_bag', 'link': reverse_lazy('admin:orders_order_changelist')},
                {'title': _('Ліди'), 'icon': 'support_agent', 'link': reverse_lazy('admin:leads_lead_changelist')},
                {'title': _('Бронювання'), 'icon': 'event', 'link': reverse_lazy('admin:booking_booking_changelist')},
                {'title': _('Калькулятор'), 'icon': 'calculate', 'link': reverse_lazy('admin:calculator_calculatorquestion_changelist')},
            ],
        },
        {
            'title': _('Користувачі'),
            'separator': True,
            'items': [
                {'title': _('Акаунти'), 'icon': 'person', 'link': reverse_lazy('admin:accounts_user_changelist')},
                {'title': _('Налаштування сайту'), 'icon': 'settings', 'link': reverse_lazy('admin:core_sitesettings_changelist')},
            ],
        },
    ]
