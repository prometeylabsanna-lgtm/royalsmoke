from __future__ import annotations

CMS_LANGUAGES: tuple[tuple[str, str, str], ...] = (
    ('uk', 'uk', 'UA'),
    ('en', 'en', 'EN'),
    ('zh-hans', 'zh_hans', '中文'),
)


def iter_cms_langs():
    for code, attr, label in CMS_LANGUAGES:
        yield code, attr, label
