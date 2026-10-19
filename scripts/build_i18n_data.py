#!/usr/bin/env python3
"""Таблиці docs/i18n/*.md → scripts/i18n_data/<мова>/<сторінка>.json (ms, fil, id, vi).

Використання:
    python3 scripts/build_i18n_data.py 01-khrom            # одна сторінка
    python3 scripts/build_i18n_data.py 01-khrom 02-golovna  # кілька
    python3 scripts/build_i18n_data.py --all               # усі сторінки

Ключ у JSON — українська фраза, значення — переклад. Збіжні українські фрази мусять мати
однаковий переклад (інакше скрипт зупиняється). Перед записом перевіряються плейсхолдери,
HTML-теги, префікси внутрішніх посилань і порожні комірки.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "i18n"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fill_i18n_po import parse_po  # noqa: E402
from i18n_sea import DATA_DIR, SEA_LANGUAGES, to_po_placeholders  # noqa: E402

# Колонки рядка після split("|"): 1 ID, 3 адреса, 5 UK, 6 EN, 7-10 ms/fil/id/vi.
ID_COL, ADDR_COL, UK_COL, FIRST_TR = 1, 3, 5, 7
PLACEHOLDER = re.compile(r"\{\{.*?\}\}|%\(\w+\)s|%s|\{\w+\}")
TAG = re.compile(r"</?\w+[^>]*>")
HREF = re.compile(r'href="([^"]*)"')
CYRILLIC = re.compile("[а-яіїєґА-ЯІЇЄҐ]")

# Рядки цих джерел не йдуть у загальні словники: у кожного власна збірка (статті блогу).
SKIP_ADDRESSES = ("blog_seed_bodies",)


def pages() -> list[str]:
    return sorted(p.stem for p in DOCS.glob("[01][0-9]-*.md"))


def parse_table(path: Path) -> list[list[str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").split("\n"):
        if re.match(r"^\| \d{4} \|", line):
            cells = [c.strip() for c in line.split("|")]
            if len(cells) != 12:
                raise SystemExit(f"{path.name}: bad cell count in {cells[ID_COL]}")
            rows.append(cells)
    return rows


def check_row(cells: list[str], lang: str, translation: str) -> list[str]:
    row_id, uk = cells[ID_COL], cells[UK_COL]
    problems = []
    if not translation:
        problems.append(f"{row_id} [{lang}] empty")
    if sorted(PLACEHOLDER.findall(translation)) != sorted(PLACEHOLDER.findall(uk)):
        problems.append(f"{row_id} [{lang}] placeholders differ")
    if TAG.findall(translation) != TAG.findall(uk):
        problems.append(f"{row_id} [{lang}] html tags differ")
    if CYRILLIC.search(translation):
        problems.append(f"{row_id} [{lang}] cyrillic left")
    uk_links, tr_links = HREF.findall(uk), HREF.findall(translation)
    if len(uk_links) != len(tr_links):
        problems.append(f"{row_id} [{lang}] link count differs")
    for src, dst in zip(uk_links, tr_links):
        if src.startswith("/") and dst != f"/{lang}{src}":
            problems.append(f"{row_id} [{lang}] link {src} -> {dst}")
    return problems


def plural_pairs() -> list[tuple[str, str]]:
    """Пари (однина, множина) укр. msgid із каталогу: для них у JSON пишемо блок "plurals"."""
    entries = parse_po(ROOT / "locale" / "en" / "LC_MESSAGES" / "django.po")
    return [(e.msgid, e.msgid_plural) for e in entries if e.is_plural]


def build_plurals(strings: dict[str, str]) -> dict[str, list[str]]:
    """{однина: [переклад однини, переклад множини]}, якщо обидві форми є на сторінці."""
    normalized = {to_po_placeholders(uk): tr for uk, tr in strings.items()}
    plurals = {}
    for singular, plural in plural_pairs():
        if singular in normalized and plural in normalized:
            plurals[singular] = [normalized[singular], normalized[plural]]
    return plurals


def build_page(page: str) -> dict[str, dict[str, str]]:
    """Повертає {мова: {укр. фраза: переклад}} для сторінки."""
    path = DOCS / f"{page}.md"
    if not path.exists():
        raise SystemExit(f"No table: {path}")
    result: dict[str, dict[str, str]] = {lang: {} for lang in SEA_LANGUAGES}
    problems: list[str] = []
    for cells in parse_table(path):
        if any(skip in cells[ADDR_COL] for skip in SKIP_ADDRESSES):
            continue
        uk = cells[UK_COL]
        for offset, lang in enumerate(SEA_LANGUAGES):
            tr = cells[FIRST_TR + offset]
            problems += check_row(cells, lang, tr)
            previous = result[lang].get(uk)
            if previous is not None and previous != tr:
                problems.append(f"{cells[ID_COL]} [{lang}] same UK, different translation")
            result[lang][uk] = tr
    if problems:
        raise SystemExit(f"{page}: {len(problems)} problem(s)\n  " + "\n  ".join(problems[:30]))
    return result


def write_page(page: str, data: dict[str, dict[str, str]]) -> None:
    for lang, strings in data.items():
        folder = DATA_DIR / lang
        folder.mkdir(parents=True, exist_ok=True)
        payload = {"page": page, "strings": dict(sorted(strings.items()))}
        plurals = build_plurals(strings)
        if plurals:
            payload["plurals"] = plurals
        text = json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
        (folder / f"{page}.json").write_text(text, encoding="utf-8")


def cross_page_conflicts() -> list[str]:
    """Одна українська фраза на різних сторінках має перекладатися однаково."""
    seen: dict[tuple[str, str], tuple[str, str]] = {}
    conflicts: list[str] = []
    for lang in SEA_LANGUAGES:
        for path in sorted((DATA_DIR / lang).glob("*.json")):
            for uk, tr in json.loads(path.read_text(encoding="utf-8"))["strings"].items():
                key = (lang, uk)
                if key in seen and seen[key][0] != tr:
                    conflicts.append(f"[{lang}] {uk[:60]!r}: {seen[key][1]} vs {path.stem}")
                seen.setdefault(key, (tr, path.stem))
    return conflicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="*", help="page names, e.g. 01-khrom")
    parser.add_argument("--all", action="store_true", help="build every page")
    args = parser.parse_args(argv)
    targets = pages() if args.all else args.pages
    if not targets:
        parser.error("name a page or use --all")
    for page in targets:
        data = build_page(page)
        write_page(page, data)
        print(f"{page}: {len(data[SEA_LANGUAGES[0]])} phrases x {len(SEA_LANGUAGES)} languages")
    conflicts = cross_page_conflicts()
    if conflicts:
        print("Cross-page conflicts:\n  " + "\n  ".join(conflicts[:20]), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
