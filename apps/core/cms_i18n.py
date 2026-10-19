"""Мови редакторів CMS: код мови, суфікс поля modeltranslation, підпис вкладки.

Суфікс поля — як у modeltranslation: дефіс → підкреслення, а для коду 'id' суфікс 'ind'
(щоб не конфліктувати з FK-атрибутами <поле>_id).
"""

from __future__ import annotations

CMS_LANGUAGES: tuple[tuple[str, str, str], ...] = (
    ('uk', 'uk', 'UA'),
    ('en', 'en', 'EN'),
    ('zh-hans', 'zh_hans', '中文'),
    ('ms', 'ms', 'MS'),
    ('fil', 'fil', 'FIL'),
    ('id', 'ind', 'ID'),
    ('vi', 'vi', 'VI'),
)


def iter_cms_langs():
    for code, attr, label in CMS_LANGUAGES:
        yield code, attr, label


def lang_fields(*bases: str) -> tuple[str, ...]:
    """('title', 'excerpt') → ('title_uk', 'title_en', …, 'excerpt_uk', …) у порядку вкладок."""
    return tuple(f'{base}_{attr}' for base in bases for _code, attr, _label in CMS_LANGUAGES)


def lang_field_set(*bases: str) -> set[str]:
    """Імена полів разом з базовим: {'body', 'body_uk', 'body_en', …} — для вибору віджетів."""
    return set(bases) | set(lang_fields(*bases))
