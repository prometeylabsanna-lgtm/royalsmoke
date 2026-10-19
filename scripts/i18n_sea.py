"""Переклади ms / fil / id / vi: завантаження з scripts/i18n_data/<мова>/*.json.

JSON-файли по одному на сторінку (01-khrom.json …) генерує scripts/build_i18n_data.py
з таблиць docs/i18n/*.md. Ключ — українська фраза, значення — переклад. Один набір даних
обслуговує і каталоги gettext (fill_i18n_po.py), і контент БД (fill_i18n_content).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'i18n_data'

SEA_LANGUAGES: tuple[str, ...] = ('ms', 'fil', 'id', 'vi')

# gettext Plural-Forms: ms, id і vi не мають множини; Filipino — дві форми.
SEA_PLURAL_FORMS: dict[str, str] = {
    'ms': 'nplurals=1; plural=0;',
    'fil': 'nplurals=2; plural=(n > 1);',
    'id': 'nplurals=1; plural=0;',
    'vi': 'nplurals=1; plural=0;',
}

_JINJA_PLACEHOLDER = re.compile(r'\{\{\s*(\w+)\s*\}\}')


def to_po_placeholders(text: str) -> str:
    """У таблицях blocktrans-змінні {{ n }}; у каталогах gettext вони %(n)s."""
    return _JINJA_PLACEHOLDER.sub(r'%(\1)s', text)


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def load_language(code: str) -> tuple[dict[str, str], dict[str, tuple[str, str]]]:
    """Повертає (рядки, множини) для мови; відсутня тека означає порожні дані."""
    if code not in SEA_LANGUAGES:
        raise ValueError(f'unknown language: {code}')
    strings: dict[str, str] = {}
    plurals: dict[str, tuple[str, str]] = {}
    folder = DATA_DIR / code
    if not folder.is_dir():
        return strings, plurals
    for path in sorted(folder.glob('*.json')):
        data = _read(path)
        for uk, tr in (data.get('strings') or {}).items():
            strings[to_po_placeholders(uk)] = to_po_placeholders(tr)
            strings.setdefault(uk, tr)
        for uk, pair in (data.get('plurals') or {}).items():
            plurals[to_po_placeholders(uk)] = (to_po_placeholders(pair[0]), to_po_placeholders(pair[1]))
    return strings, plurals


_CYRILLIC = re.compile('[а-яіїєґА-ЯІЇЄҐ]')
_P_WRAPPER = re.compile(r'^<p>(.*)</p>$', re.S)
_cache: dict[str, dict[str, str]] = {}
_templates_cache: dict[str, list[tuple[re.Pattern, str]]] = {}
_BRACE_FIELD = re.compile(r'(?<!\{)\{(\w+)\}(?!\})')


def _strings(code: str) -> dict[str, str]:
    if code not in _cache:
        _cache[code] = load_language(code)[0]
    return _cache[code]


def clear_cache() -> None:
    _cache.clear()
    _templates_cache.clear()
    _flat_cache.clear()


def _templates(code: str) -> list[tuple[re.Pattern, str]]:
    """Шаблони таблиці з полями {name}, {brand}: регулярка за українським текстом → переклад."""
    if code not in _templates_cache:
        found = []
        for uk, tr in _strings(code).items():
            if not _BRACE_FIELD.search(uk):
                continue
            pattern, last = [], 0
            for match in _BRACE_FIELD.finditer(uk):
                pattern.append(re.escape(uk[last:match.start()]))
                pattern.append(f'(?P<{match.group(1)}>.+?)')
                last = match.end()
            pattern.append(re.escape(uk[last:]))
            found.append((len(uk), re.compile('^' + ''.join(pattern) + '$', re.S), tr))
        found.sort(key=lambda item: -item[0])
        _templates_cache[code] = [(rx, tr) for _n, rx, tr in found]
    return _templates_cache[code]


def _fill_template(code: str, text: str) -> str | None:
    for regex, translation in _templates(code):
        match = regex.match(text)
        if match:
            result = translation
            for name, value in match.groupdict().items():
                # Назви в полях ({name}, {brand}) беруть власний переклад, якщо він є в таблиці.
                translated = _find(_strings(code), value) if _CYRILLIC.search(value) else None
                result = result.replace('{' + name + '}', translated or value)
            return result
    return None


def _squash(text: str) -> str:
    """Збіг не залежить від переносів рядка: у БД абзаци розділені \\n\\n, у таблиці — один рядок."""
    return re.sub(r'\s+', ' ', text).strip()


_flat_cache: dict[str, dict[str, str]] = {}


def _flat(code: str) -> dict[str, str]:
    if code not in _flat_cache:
        _flat_cache[code] = {_squash(uk): tr for uk, tr in _strings(code).items()}
    return _flat_cache[code]


def _find(strings: dict[str, str], text: str) -> str | None:
    for key in (text, text.replace("ʼ", "'"), text.replace("'", "ʼ"), to_po_placeholders(text)):
        if key in strings:
            return strings[key]
    return None


_HTML_BLOCK = re.compile(r'<(h1|h2|h3|h4|p|li|blockquote)>(.*?)</\1>', re.S)


def _lookup(code: str, text: str) -> str | None:
    return _find(_strings(code), text) or _flat(code).get(_squash(text)) or _fill_template(code, text)


def _translate_html(raw: str) -> dict[str, str] | None:
    """Цілий HTML політики/доставки: кожен заголовок і абзац є окремим рядком таблиці."""
    matches = list(_HTML_BLOCK.finditer(raw))
    if not matches:
        return None
    pieces: list[dict[str, str]] = []
    for match in matches:
        inner = _squash(match.group(2))
        found = {code: _lookup(code, inner) for code in SEA_LANGUAGES}
        if not all(found.values()):
            return None
        pieces.append(found)

    out: dict[str, str] = {}
    for code in SEA_LANGUAGES:
        texts = iter(piece[code] for piece in pieces)

        def sub(match: re.Match, pending: iter = texts) -> str:
            return f'<{match.group(1)}>{next(pending)}</{match.group(1)}>'

        out[code] = _HTML_BLOCK.sub(sub, raw)
    return out


def translate(text: str | None) -> dict[str, str] | None:
    """Переклад українського тексту CMS/БД на ms, fil, id, vi за точним збігом.

    TinyMCE-обгортка <p>…</p> не заважає збігу й повертається назад. Тексти без кирилиці
    (числа, бренди) однакові в усіх мовах. Немає збігу — None (переклад ще не завантажено).
    """
    raw = (text or '').strip()
    if not raw:
        return None
    wrapped = _P_WRAPPER.match(raw)
    for candidate, wrap in ((raw, False), (wrapped.group(1).strip(), True) if wrapped else (None, False)):
        if not candidate:
            continue
        found = {code: _lookup(code, candidate) for code in SEA_LANGUAGES}
        if all(found.values()):
            return {code: (f'<p>{tr}</p>' if wrap else tr) for code, tr in found.items()}
    html = _translate_html(raw)
    if html:
        return html
    if not _CYRILLIC.search(raw):
        return {code: raw for code in SEA_LANGUAGES}
    return None
