"""Одноразова збірка HTML body доставки з карток / legacy-блоків."""

from __future__ import annotations

from django.utils.html import escape

from apps.core.legal_delivery_body import (
    DELIVERY_BODY_EN,
    DELIVERY_BODY_UK,
    DELIVERY_BODY_ZH,
)
from apps.core.models import DeliveryCard, SiteBlock


def _escape_text(value: str) -> str:
    return escape((value or '').strip())


def _block_text(key: str, attr: str = 'text_html') -> str:
    block = SiteBlock.objects.filter(page='delivery', key=key).first()
    if block is None:
        return ''
    raw = (getattr(block, attr, None) or block.text_html or '').strip()
    return raw


def build_delivery_body_html(
    *,
    regions: list[DeliveryCard] | None = None,
    payments: list[DeliveryCard] | None = None,
    h2: str = '',
    pay_h2: str = '',
    pay_intro: str = '',
) -> str:
    """Збирає HTML з карток і заголовків секцій (якщо є)."""
    region_qs = regions
    if region_qs is None:
        region_qs = list(
            DeliveryCard.objects.filter(
                kind=DeliveryCard.Kind.REGION, is_active=True,
            ).order_by('sort_order', 'pk')
        )
    payment_qs = payments
    if payment_qs is None:
        payment_qs = list(
            DeliveryCard.objects.filter(
                kind=DeliveryCard.Kind.PAYMENT, is_active=True,
            ).order_by('sort_order', 'pk')
        )

    h2 = (h2 or _block_text('h2') or 'Доставка').strip()
    pay_h2 = (pay_h2 or _block_text('pay_h2') or 'Оплата').strip()
    pay_intro = (pay_intro or _block_text('pay_intro') or '').strip()

    parts: list[str] = [f'<h2>{_escape_text(h2)}</h2>']
    if region_qs:
        for card in region_qs:
            title = (card.title or '').strip()
            text = (card.text or '').strip()
            if title:
                parts.append(f'<h3>{_escape_text(title)}</h3>')
            if text:
                parts.append(f'<p>{_escape_text(text)}</p>')
    else:
        return DELIVERY_BODY_UK

    parts.append(f'<h2>{_escape_text(pay_h2)}</h2>')
    if pay_intro:
        parts.append(f'<p>{_escape_text(pay_intro)}</p>')
    if payment_qs:
        parts.append('<ul>')
        for card in payment_qs:
            title = (card.title or '').strip()
            text = (card.text or '').strip()
            label = _escape_text(title) if title else 'Оплата'
            detail = _escape_text(text)
            if detail:
                parts.append(f'<li><strong>{label}</strong> — {detail}</li>')
            else:
                parts.append(f'<li><strong>{label}</strong></li>')
        parts.append('</ul>')
    return '\n'.join(parts)


def ensure_delivery_body_block(*, force: bool = False) -> bool:
    """
    Створює/заповнює delivery.body з карток (або дефолту).
    Не перезаписує непорожній body, якщо force=False.
    """
    body_block, _created = SiteBlock.objects.get_or_create(
        page='delivery',
        key='body',
        defaults={
            'label': 'Текст сторінки',
            'content_type': SiteBlock.ContentType.TEXT,
            'text_html': '',
            'is_active': True,
        },
    )
    current = (body_block.text_html or '').strip()
    if current and not force:
        changed = False
        if not (getattr(body_block, 'text_html_uk', None) or '').strip():
            body_block.text_html_uk = current
            changed = True
        if not (getattr(body_block, 'text_html_en', None) or '').strip():
            body_block.text_html_en = DELIVERY_BODY_EN
            changed = True
        if not (getattr(body_block, 'text_html_zh_hans', None) or '').strip():
            body_block.text_html_zh_hans = DELIVERY_BODY_ZH
            changed = True
        if changed:
            body_block.save()
        return changed

    has_cards = DeliveryCard.objects.filter(is_active=True).exists()
    html_uk = build_delivery_body_html() if has_cards else DELIVERY_BODY_UK
    body_block.label = 'Текст сторінки'
    body_block.content_type = SiteBlock.ContentType.TEXT
    body_block.text_html = html_uk
    body_block.text_html_uk = html_uk
    if force or not (getattr(body_block, 'text_html_en', None) or '').strip():
        body_block.text_html_en = DELIVERY_BODY_EN
    if force or not (getattr(body_block, 'text_html_zh_hans', None) or '').strip():
        body_block.text_html_zh_hans = DELIVERY_BODY_ZH
    body_block.is_active = True
    body_block.save()
    return True


def ensure_delivery_header_blocks() -> None:
    """Гарантує title/lead/bg для сторінки доставки."""
    from apps.core.block_defaults import BLOCK_DEFAULTS, BLOCK_FIELD_LABELS

    specs = (
        ('title', 'text'),
        ('lead', 'text'),
        ('bg', 'image'),
    )
    for key, ctype in specs:
        SiteBlock.objects.get_or_create(
            page='delivery',
            key=key,
            defaults={
                'label': BLOCK_FIELD_LABELS.get(('delivery', key), key),
                'content_type': ctype,
                'text_html': str(BLOCK_DEFAULTS.get(('delivery', key), '')),
                'is_active': True,
            },
        )
