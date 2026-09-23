from __future__ import annotations

from apps.core.models import DeliveryCard, SiteBlock

DELIVERY_REGION_DEFAULTS: tuple[dict[str, str | int], ...] = (
    {
        'title': 'Київ',
        'text': (
            'Курʼєрська доставка того ж дня при замовленні до 15:00. '
            'Самовивіз зі шоуруму.'
        ),
        'sort_order': 0,
    },
    {
        'title': 'Україна',
        'text': 'Нова Пошта — 1–2 дні. Сигари пакуємо в термобокси зі страхуванням.',
        'sort_order': 1,
    },
    {
        'title': 'ЄС',
        'text': 'Міжнародна доставка — 3–5 робочих днів. Умови уточнюйте у менеджера.',
        'sort_order': 2,
    },
    {
        'title': 'Способи доставки',
        'text': 'Нова Пошта, курʼєр або самовивіз — обираєте під час оформлення.',
        'sort_order': 3,
    },
)

DELIVERY_PAYMENT_DEFAULTS: tuple[dict[str, str | int], ...] = (
    {
        'title': 'Онлайн оплата',
        'text': 'банківською карткою через платіжний сервіс.',
        'sort_order': 0,
    },
    {
        'title': 'Оплата при отриманні',
        'text': 'готівкою або карткою курʼєру / у відділенні.',
        'sort_order': 1,
    },
    {
        'title': 'Безготівковий розрахунок',
        'text': 'для юридичних осіб та B2B-замовлень за рахунком.',
        'sort_order': 2,
    },
)

_LEGACY_REGION_KEYS: tuple[tuple[str, str], ...] = (
    ('kyiv_title', 'kyiv_text'),
    ('ua_title', 'ua_text'),
    ('eu_title', 'eu_text'),
    ('methods_title', 'methods_text'),
)
_LEGACY_PAYMENT_KEYS: tuple[tuple[str, str], ...] = (
    ('pay_online_title', 'pay_online_text'),
    ('pay_cod_title', 'pay_cod_text'),
    ('pay_b2b_title', 'pay_b2b_text'),
)


def _block_text(key: str) -> str:
    block = SiteBlock.objects.filter(page='delivery', key=key, is_active=True).first()
    if block and (block.text_html or '').strip():
        return block.text_html.strip()
    return ''


def _seed_kind(kind: str, defaults: tuple[dict, ...], legacy_pairs: tuple[tuple[str, str], ...]) -> int:
    if DeliveryCard.objects.filter(kind=kind).exists():
        return 0
    created = 0
    for idx, item in enumerate(defaults):
        title = str(item['title'])
        text = str(item['text'])
        if idx < len(legacy_pairs):
            t_key, x_key = legacy_pairs[idx]
            title = _block_text(t_key) or title
            text = _block_text(x_key) or text
        DeliveryCard.objects.create(
            kind=kind,
            title=title,
            text=text,
            sort_order=int(item.get('sort_order', idx)),
            is_active=True,
        )
        created += 1
    return created


def ensure_delivery_cards() -> int:
    """Ідемпотентний seed карток; підтягує текст зі старих SiteBlock, якщо є."""
    n = 0
    n += _seed_kind(DeliveryCard.Kind.REGION, DELIVERY_REGION_DEFAULTS, _LEGACY_REGION_KEYS)
    n += _seed_kind(DeliveryCard.Kind.PAYMENT, DELIVERY_PAYMENT_DEFAULTS, _LEGACY_PAYMENT_KEYS)
    return n


def active_delivery_regions():
    ensure_delivery_cards()
    return list(DeliveryCard.objects.filter(kind=DeliveryCard.Kind.REGION, is_active=True))


def active_delivery_payments():
    ensure_delivery_cards()
    return list(DeliveryCard.objects.filter(kind=DeliveryCard.Kind.PAYMENT, is_active=True))
