#!/usr/bin/env python3
"""Збирає locale_django/fil/LC_MESSAGES/django.po/.mo з scripts/django_fil_messages.py.

Каталог лежить окремо від locale/, щоб makemessages його не чіпав. Кожен msgid перевіряється
за англійським каталогом Django: опечатка в оригіналі зупиняє збірку.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import django

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from django_fil_messages import MESSAGES  # noqa: E402
from fill_i18n_po import format_po_string  # noqa: E402

TARGET = ROOT / 'locale_django' / 'fil' / 'LC_MESSAGES'
HEADER = (
    'Project-Id-Version: Royal Smoke (Django built-in messages)\n'
    'Language: fil\n'
    'MIME-Version: 1.0\n'
    'Content-Type: text/plain; charset=UTF-8\n'
    'Content-Transfer-Encoding: 8bit\n'
    'Plural-Forms: nplurals=2; plural=(n > 1);\n'
)


def _unquote(block: str) -> str:
    raw = ''.join(re.findall(r'"((?:[^"\\]|\\.)*)"', block))
    return raw.replace('\\"', '"').replace('\\\\', '\\')


def django_english_msgids() -> dict[str, str | None]:
    """msgid → msgid_plural (або None) з англійських каталогів Django."""
    base = Path(django.__file__).parent
    found: dict[str, str | None] = {}
    for path in (base / 'conf/locale/en/LC_MESSAGES/django.po', *base.glob('contrib/*/locale/en/LC_MESSAGES/django.po')):
        text = path.read_text(encoding='utf-8')
        for block in re.split(r'\n\n+', text):
            single = re.search(r'^msgid ((?:".*"\n?)+)', block, re.M)
            if not single:
                continue
            plural = re.search(r'^msgid_plural ((?:".*"\n?)+)', block, re.M)
            found[_unquote(single.group(1))] = _unquote(plural.group(1)) if plural else None
    return found


def build() -> None:
    known = django_english_msgids()
    unknown = [msgid for msgid in MESSAGES if msgid not in known]
    if unknown:
        raise SystemExit('Not in Django catalogs:\n  ' + '\n  '.join(unknown))
    lines = ['msgid ""', 'msgstr ""'] + [f'"{part}\\n"' for part in HEADER.rstrip('\n').split('\n')] + ['']
    for msgid, value in MESSAGES.items():
        if '%' in msgid:
            lines.append('#, python-format')
        if isinstance(value, tuple):
            lines += format_po_string(msgid, 'msgid')
            plural_id = known[msgid]
            if not plural_id:
                raise SystemExit(f'Django msgid has no plural form: {msgid!r}')
            lines += format_po_string(plural_id, 'msgid_plural')
            for index, text in enumerate(value):
                lines += format_po_string(text, f'msgstr[{index}]')
        else:
            lines += format_po_string(msgid, 'msgid')
            lines += format_po_string(value, 'msgstr')
        lines.append('')
    TARGET.mkdir(parents=True, exist_ok=True)
    po = TARGET / 'django.po'
    po.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    subprocess.run(['msgfmt', '--check-format', '-o', str(TARGET / 'django.mo'), str(po)], check=True)
    print(f'{len(MESSAGES)} messages -> {po.relative_to(ROOT)}')


if __name__ == '__main__':
    build()
