"""Українські назви місць латиницею (КМУ 2010) для вітрин, крім української.

На українській мові назви Нової Пошти лишаються кирилицею. В усіх інших мовах
місто, область і відділення показуються транслітерацією: Київ → Kyiv.
"""

from __future__ import annotations

from django.conf import settings
from django.utils.translation import get_language

# Літера → латиниця. є/ї/й/ю/я залежать від початку слова.
_PLAIN = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ь': '', 'ъ': '', 'ы': 'y', 'э': 'e', 'ё': 'e',
}
_WORD_START = {'є': 'ye', 'ї': 'yi', 'й': 'y', 'ю': 'yu', 'я': 'ya'}
_WORD_MID = {'є': 'ie', 'ї': 'i', 'й': 'i', 'ю': 'iu', 'я': 'ia'}
_APOSTROPHE = frozenset("'ʼ’")


def transliterate_uk(text: str) -> str:
    """Кирилицю в латиницю; латиницю, цифри й розділові знаки не чіпає."""
    out: list[str] = []
    word_start = True
    for char in text or '':
        lower = char.lower()
        if lower in _WORD_START:
            piece = _WORD_START[lower] if word_start else _WORD_MID[lower]
        elif lower in _PLAIN:
            piece = _PLAIN[lower]
        elif char in _APOSTROPHE:
            continue
        else:
            out.append(char)
            word_start = not char.isalpha()
            continue
        if char.isupper() and piece:
            piece = piece[0].upper() + piece[1:]
        out.append(piece)
        word_start = False
    return ''.join(out)


def place_name(text: str, lang: str | None = None) -> str:
    """Назву місця: українською як є, іншими мовами — транслітерацією."""
    raw = text or ''
    active = (lang if lang is not None else get_language()) or settings.LANGUAGE_CODE
    if active.lower().startswith('uk'):
        return raw
    return transliterate_uk(raw)
