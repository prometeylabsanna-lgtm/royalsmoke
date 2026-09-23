"""Логіка підбору сигар за параметрами калькулятора."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy

from apps.catalog.models import Product
from apps.core.currency import convert_from_uah, get_currency

COUNTRY_LABELS = {
    'cuba': _lazy('Куба'),
    'nicaragua': _lazy('Нікарагуа'),
    'dominican': _lazy('Домінікана'),
    'mexico': _lazy('Мексика'),
}

FORMAT_TERMS = {
    'petit': ('petit', 'petit robusto'),
    'robusto': ('robusto',),
    'toro': ('toro',),
    'churchill': ('churchill',),
}

STRENGTH_LABELS = dict(Product.Strength.choices)

BUDGET_LABELS = {
    '0-1000': 'до 1000 ₴',
    '1000-2000': '1000—2000 ₴',
    '2000-3500': '2000—3500 ₴',
    'any': 'без обмежень',
}


@dataclass(frozen=True)
class CalcHit:
    product: Product
    score: int
    reasons: list[str]


def parse_budget(raw: str | None) -> tuple[Decimal | None, Decimal | None]:
    """Повертає (min, max) включно. None = без межі."""
    if not raw or raw == 'any':
        return None, None
    raw = raw.strip()
    if '-' in raw and not raw.startswith('-'):
        left, _, right = raw.partition('-')
        try:
            lo = Decimal(left) if left else None
            hi = Decimal(right) if right else None
            return lo, hi
        except (InvalidOperation, ValueError):
            return None, None
    try:
        return None, Decimal(raw)
    except (InvalidOperation, ValueError):
        return None, None


def _format_q(fmt: str) -> Q | None:
    terms = FORMAT_TERMS.get(fmt)
    if not terms:
        terms = (fmt,)
    q = Q()
    for term in terms:
        q |= Q(name__icontains=term) | Q(short_story__icontains=term)
    return q


def _price_in_range(price: Decimal, lo: Decimal | None, hi: Decimal | None) -> bool:
    if lo is not None and price < lo:
        return False
    if hi is not None and price > hi:
        return False
    return True


def _score_product(
    product: Product,
    *,
    strength: str | None,
    country_label: str | None,
    fmt: str | None,
    budget_lo: Decimal | None,
    budget_hi: Decimal | None,
) -> CalcHit:
    score = 0
    reasons: list[str] = []
    price = product.display_price

    if strength and product.strength == strength:
        score += 40
        reasons.append(_('міцність %(s)s') % {'s': str(STRENGTH_LABELS.get(strength, strength)).lower()})
    elif strength and product.strength:
        # сусідні рівні — частковий збіг
        order = ['mild', 'medium', 'medium_full', 'full']
        try:
            dist = abs(order.index(product.strength) - order.index(strength))
            if dist == 1:
                score += 12
        except ValueError:
            pass

    if country_label:
        if country_label.lower() in (product.country or '').lower():
            score += 30
            reasons.append(_('країна %(c)s') % {'c': product.country})
    else:
        score += 5

    if fmt:
        terms = FORMAT_TERMS.get(fmt, (fmt,))
        haystack = f'{(product.name or "")} {(product.short_story or "")}'.lower()
        if any(t in haystack for t in terms):
            score += 25
            label = {
                'petit': 'Petit Robusto',
                'robusto': 'Robusto',
                'toro': 'Toro',
                'churchill': 'Churchill',
            }.get(fmt, fmt)
            reasons.append(_('формат %(f)s') % {'f': label})

    if budget_lo is None and budget_hi is None:
        score += 5
    elif _price_in_range(price, budget_lo, budget_hi):
        score += 35
        reasons.append(
            _('у бюджеті (%(p)s %(symbol)s)')
            % {'p': convert_from_uah(price), 'symbol': get_currency()['symbol']}
        )
    elif budget_hi is not None and price <= budget_hi * Decimal('1.15'):
        score -= 8
    else:
        score -= 40

    if not reasons:
        reasons.append(_('близький за профілем асортименту'))

    return CalcHit(product=product, score=score, reasons=reasons)


def recommend_products(answers: dict, limit: int = 3) -> list[CalcHit]:
    strength = (answers.get('strength') or '').strip() or None
    fmt = (answers.get('format') or '').strip().lower() or None
    country_key = (answers.get('country') or '').strip().lower() or None
    country_label = str(COUNTRY_LABELS[country_key]) if country_key in COUNTRY_LABELS else None
    budget_lo, budget_hi = parse_budget(answers.get('budget'))

    qs = Product.objects.on_storefront().with_relations().filter(
        category__slug='cigars',
    )

    # мʼякий попередній фільтр, щоб не сканувати весь каталог
    hard = Q()
    if strength:
        hard &= Q(strength=strength)
    if country_label:
        hard &= Q(country__icontains=country_label)
    if fmt:
        fq = _format_q(fmt)
        if fq is not None:
            hard &= fq
    if budget_hi is not None:
        hard &= Q(base_price__lte=budget_hi * Decimal('1.25'))
    if budget_lo is not None:
        hard &= Q(base_price__gte=budget_lo * Decimal('0.75'))

    candidates = list(qs.filter(hard).distinct()[:40])
    if len(candidates) < limit * 3:
        extra = list(
            qs.exclude(pk__in=[p.pk for p in candidates])[: 40 - len(candidates)]
        )
        candidates.extend(extra)

    scored = [
        _score_product(
            p,
            strength=strength,
            country_label=country_label,
            fmt=fmt,
            budget_lo=budget_lo,
            budget_hi=budget_hi,
        )
        for p in candidates
    ]
    scored.sort(key=lambda h: (-h.score, h.product.display_price, h.product.name))
    return scored[:limit]
