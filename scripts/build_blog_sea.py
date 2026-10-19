#!/usr/bin/env python3
"""Збирає HTML тіл статей блогу для ms / fil / id / vi з docs/i18n/08-blog.md.

Структура тегів береться з української статті. Внутрішній текст кожного блоку
замінюється перекладом того самого рядка таблиці. Результат:
apps/pages/blog_seed_ms.py, blog_seed_fil.py, blog_seed_id.py, blog_seed_vi.py.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from apps.pages.blog_seed_bodies1 import POST_BODIES as BODIES_1  # noqa: E402
from apps.pages.blog_seed_bodies2 import POST_BODIES as BODIES_2  # noqa: E402
from apps.pages.blog_seed_extra import EXTRA_UK  # noqa: E402

LANGS = ('ms', 'fil', 'id', 'vi')
# Колонки перекладу після split("|"): 7 ms, 8 fil, 9 id, 10 vi.
LANG_COL = {'ms': 7, 'fil': 8, 'id': 9, 'vi': 10}
SLUGS = (
    'yak-obraty-pershu-sygaru',
    'yak-zberigaty-sygary-humidora',
    'aksessuary-dlya-sygar-katter-zapalnychka',
    'yak-chytaty-vitolu-micnist-kilce',
)
BLOCK = re.compile(r'<(h1|h2|h3|h4|p|li|blockquote)>(.*?)</\1>', re.S)
TAG_RE = re.compile(r'</?\w+[^>]*>')
HREF_PREFIX = re.compile(r'href="/(?:ms|fil|id|vi)/')


def table_body_rows() -> list[list[str]]:
    rows = []
    for line in (ROOT / 'docs/i18n/08-blog.md').read_text(encoding='utf-8').split('\n'):
        if not re.match(r'^\| \d{4} \|', line):
            continue
        cells = [c.strip() for c in line.split('|')]
        if 'blog_seed_bodies' in cells[3]:
            rows.append(cells)
    return rows


def uk_blocks(html: str) -> list[tuple[str, str]]:
    out = []
    for match in BLOCK.finditer(html):
        text = re.sub(r'\s+', ' ', match.group(2)).strip()
        out.append((match.group(1), text))
    return out


def rebuild(html: str, texts: list[str]) -> str:
    it = iter(texts)
    count = 0

    def sub(match: re.Match) -> str:
        nonlocal count
        count += 1
        return f'<{match.group(1)}>{next(it)}</{match.group(1)}>'

    result = BLOCK.sub(sub, html)
    if count != len(texts):
        raise SystemExit(f'block count {count} != translations {len(texts)}')
    return result.strip() + '\n'


def groups() -> list[list[list[str]]]:
    rows = table_body_rows()
    found: list[list[list[str]]] = []
    current: list[list[str]] = []
    for cells in rows:
        # Нова стаття починається з абзацу після метаданих; межі відомі за ID.
        if cells[1] in {'0778', '0833', '0887'} and current:
            found.append(current)
            current = []
        current.append(cells)
    found.append(current)
    if len(found) != len(SLUGS):
        raise SystemExit(f'expected {len(SLUGS)} articles, got {len(found)}')
    return found


def main() -> None:
    uk_html = {**BODIES_1, **BODIES_2}
    per_lang: dict[str, dict[str, str]] = {lang: {} for lang in LANGS}
    for slug, rows in zip(SLUGS, groups()):
        html = uk_html[slug]['uk'] + EXTRA_UK.get(slug, '')
        blocks = uk_blocks(html)
        if len(blocks) != len(rows):
            raise SystemExit(f'{slug}: uk {len(blocks)} rows {len(rows)}')
        for lang in LANGS:
            texts = []
            for (tag, uk), cells in zip(blocks, rows):
                if cells[5] != uk:
                    raise SystemExit(f'{slug} {cells[1]}: table UK != HTML block')
                tr = cells[LANG_COL[lang]]
                bare = HREF_PREFIX.sub('href="/', tr)
                if TAG_RE.findall(bare) != TAG_RE.findall(uk):
                    raise SystemExit(f'{slug} {cells[1]} [{lang}]: tags differ')
                texts.append(tr)
            per_lang[lang][slug] = rebuild(html, texts)
        print(f'{slug}: {len(blocks)} blocks')

    for lang, bodies in per_lang.items():
        parts = [
            '"""Тіла статей блогу. Згенеровано scripts/build_blog_sea.py з docs/i18n/08-blog.md."""',
            '',
            'BODIES = {',
        ]
        for slug, html in bodies.items():
            parts.append(f'    {slug!r}: """')
            parts.append(html.rstrip('\n'))
            parts.append('""",')
        parts.append('}')
        parts.append('')
        path = ROOT / 'apps/pages' / f'blog_seed_{lang}.py'
        path.write_text('\n'.join(parts), encoding='utf-8')
        print(f'wrote {path.name}: {path.read_text(encoding="utf-8").count(chr(10))} lines')


if __name__ == '__main__':
    main()
