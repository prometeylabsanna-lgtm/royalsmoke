"""Парсер таблиць docs/i18n/mobile-20261102/11-mobile-*.md (M001–M159)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / 'docs' / 'i18n' / 'mobile-20261102'

# Код мови в таблиці → код modeltranslation / API.
LANGS: tuple[str, ...] = ('uk', 'en', 'zh-hans', 'ms', 'fil', 'id', 'vi')
_COL = {
    'uk': 5,
    'en': 6,
    'zh-hans': 7,
    'ms': 8,
    'fil': 9,
    'id': 10,
    'vi': 11,
}


@dataclass(frozen=True)
class Phrase:
    id: str
    where: str
    address: str
    role: str
    action: str
    texts: dict[str, str]
    status: str

    def raw(self, lang: str) -> str:
        return self.texts[lang]

    def text(self, lang: str) -> str:
        """Текст для застосунку: літеральна послідовність \\n у таблиці стає переносом."""
        return self.texts[lang].replace('\\n', '\n')


def load_phrases(docs: Path | None = None) -> list[Phrase]:
    folder = docs or DOCS
    files = sorted(folder.glob('11-mobile-*.md'))
    if len(files) != 4:
        raise FileNotFoundError(f'Очікувались 4 файли 11-mobile-*.md у {folder}')
    phrases: list[Phrase] = []
    for path in files:
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.startswith('| M'):
                continue
            cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
            if len(cells) != 13:
                raise ValueError(f'{path.name}: {cells[0] if cells else "?"} має {len(cells)} колонок')
            phrases.append(
                Phrase(
                    id=cells[0],
                    where=cells[1],
                    address=cells[2],
                    role=cells[3],
                    action=cells[4],
                    texts={lang: cells[_COL[lang]] for lang in LANGS},
                    status=cells[12],
                )
            )
    phrases.sort(key=lambda item: item.id)
    ids = [item.id for item in phrases]
    expected = [f'M{i:03d}' for i in range(1, 160)]
    if ids != expected:
        missing = [item for item in expected if item not in ids]
        extra = [item for item in ids if item not in expected]
        raise ValueError(f'Очікувались M001–M159. Немає: {missing}. Зайві: {extra}')
    for item in phrases:
        if '{date}' in item.texts['uk']:
            for lang in LANGS:
                if '{date}' not in item.texts[lang]:
                    raise ValueError(f'{item.id} {lang}: втрачено плейсхолдер {{date}}')
    return phrases


def by_id(phrases: list[Phrase] | None = None) -> dict[str, Phrase]:
    return {item.id: item for item in (phrases if phrases is not None else load_phrases())}
