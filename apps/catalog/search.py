"""Catalog search: sanitize, literal match, UA↔LAT translit for name/brand."""

from __future__ import annotations

import re
from functools import reduce
from operator import or_

from django.db.models import Q

SEARCH_MAX_LEN = 100
SEARCH_MIN_LEN = 1
SUGGEST_MIN_LEN = 2

# Ukrainian (+ shared Cyrillic) → Latin
_CYR_TO_LAT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
    'є': 'ye', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y',
    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
    'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'yu', 'я': 'ya', 'ъ': '', 'ы': 'y',
    'э': 'e',
}

# Longer digraphs first for Latin → Cyrillic
_LAT_TO_CYR_MULTI = (
    ('shch', 'щ'),
    ('zh', 'ж'),
    ('kh', 'х'),
    ('ts', 'ц'),
    ('ch', 'ч'),
    ('sh', 'ш'),
    ('yu', 'ю'),
    ('ya', 'я'),
    ('ye', 'є'),
    ('yi', 'ї'),
)
_LAT_TO_CYR = {
    'a': 'а', 'b': 'б', 'c': 'к', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'ґ',
    'h': 'г', 'i': 'і', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
    'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
    'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'и', 'z': 'з',
}


def sanitize_search_query(raw) -> str:
    if raw is None:
        return ''
    text = str(raw).replace('\x00', '')
    text = ' '.join(text.split())
    if len(text) > SEARCH_MAX_LEN:
        text = text[:SEARCH_MAX_LEN]
    return text.strip()


def cyr_to_lat(text: str) -> str:
    out: list[str] = []
    for ch in text:
        lower = ch.lower()
        if lower in _CYR_TO_LAT:
            mapped = _CYR_TO_LAT[lower]
            if ch.isupper() and mapped:
                mapped = mapped[0].upper() + mapped[1:]
            out.append(mapped)
        else:
            out.append(ch)
    return ''.join(out)


def lat_to_cyr(text: str) -> str:
    lower = text.lower()
    out: list[str] = []
    i = 0
    while i < len(lower):
        matched = False
        for latin, cyr in _LAT_TO_CYR_MULTI:
            if lower.startswith(latin, i):
                out.append(cyr)
                i += len(latin)
                matched = True
                break
        if matched:
            continue
        ch = lower[i]
        out.append(_LAT_TO_CYR.get(ch, text[i]))
        i += 1
    return ''.join(out)


def search_variants(query: str) -> list[str]:
    q = sanitize_search_query(query)
    if not q:
        return []
    variants: list[str] = []
    seen: set[str] = set()
    for candidate in (q, cyr_to_lat(q), lat_to_cyr(q)):
        candidate = sanitize_search_query(candidate)
        if not candidate:
            continue
        key = candidate.casefold()
        if key in seen:
            continue
        seen.add(key)
        variants.append(candidate)
    return variants


def product_search_q(raw, *, fields: tuple[str, ...] = ('name', 'brand__name')) -> Q:
    """Literal, case-insensitive match (iregex + re.escape → %/_ not wildcards)."""
    variants = search_variants(raw)
    if not variants:
        return Q()
    parts: list[Q] = []
    for variant in variants:
        pattern = re.escape(variant)
        field_q = Q()
        for field in fields:
            field_q |= Q(**{f'{field}__iregex': pattern})
        parts.append(field_q)
    return reduce(or_, parts)
