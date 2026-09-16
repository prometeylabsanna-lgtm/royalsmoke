from __future__ import annotations

CMS_LANGUAGES: tuple[tuple[str, str, str], ...] = (
    ('uk', 'uk', 'UA'),
    ('en', 'en', 'EN'),
    ('zh-hans', 'zh_hans', '中文'),
)


def lang_attr(code: str) -> str:
    return code.replace('-', '_')


def translated_attr(field: str, code: str) -> str:
    return f'{field}_{lang_attr(code)}'


def iter_cms_langs():
    for code, attr, label in CMS_LANGUAGES:
        yield code, attr, label
