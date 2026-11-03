"""Ідемпотентні правки джерельних таблиць мобільного довідника. Пише CHANGES.md."""

from __future__ import annotations

from pathlib import Path

from mobile_tables import DOCS, LANGS, _COL

M111_UK = (
    'Довідник створено для дорослої аудиторії 21+; він розповідає про культуру, '
    'походження та атмосферу простору, який ми підтримуємо.'
)
M111_EN = (
    'The guide is created for an adult audience of 21+ and covers the culture, '
    'origins, and atmosphere of the space we support.'
)

M036 = {
    'uk': 'Royal Smoke — інформаційний довідник дому бренду. Застосунок призначений для осіб 21+.',
    'en': 'Royal Smoke is an informational guide to the brand house. The app is intended for people aged 21+.',
    'zh-hans': 'Royal Smoke 是品牌之家的信息指南。本应用面向21岁及以上人士。',
    'ms': (
        'Royal Smoke ialah panduan maklumat tentang rumah jenama. '
        'Aplikasi ini ditujukan untuk mereka yang berumur 21 tahun ke atas.'
    ),
    'fil': (
        'Ang Royal Smoke ay isang gabay ng impormasyon tungkol sa bahay ng brand. '
        'Ang app ay para sa mga may edad na 21 pataas.'
    ),
    'id': (
        'Royal Smoke adalah panduan informasi tentang rumah merek. '
        'Aplikasi ini ditujukan bagi orang berusia 21 tahun ke atas.'
    ),
    'vi': (
        'Royal Smoke là cẩm nang thông tin về ngôi nhà thương hiệu. '
        'Ứng dụng dành cho người từ 21 tuổi trở lên.'
    ),
}


def _brand_range(mid: str) -> bool:
    return 'M040' <= mid <= 'M089'


def _fix_cells(cells: list[str]) -> list[str]:
    mid = cells[0]
    updated = cells[:]
    if mid == 'M098':
        updated[5] = updated[5].replace('допомогають', 'допомагають')
    if mid == 'M111':
        updated[5] = M111_UK
        updated[6] = M111_EN
    if 'Турренте' in updated[5]:
        updated[5] = updated[5].replace('Турренте', 'Туррент')
    if _brand_range(mid):
        for src, dst in (
            ('ДІМ БРЕНДІВ', 'ДІМ БРЕНДУ'),
            ('Дім брендів', 'Дім бренду'),
            ('дім брендів', 'дім бренду'),
        ):
            updated[5] = updated[5].replace(src, dst)
        return updated
    if mid == 'M015':
        return updated
    if mid == 'M036':
        for lang, text in M036.items():
            updated[_COL[lang]] = text
        return updated
    for src, dst in (
        ('брендів дому', 'дому бренду'),
        ('Брендів дому', 'Дому бренду'),
        ('ДІМ БРЕНДІВ', 'ДІМ БРЕНДУ'),
        ('Дім брендів', 'Дім бренду'),
        ('дім брендів', 'дім бренду'),
    ):
        updated[5] = updated[5].replace(src, dst)
    return updated


def _render(cells: list[str]) -> str:
    return '| ' + ' | '.join(cells) + ' |'


def apply() -> list[str]:
    notes: list[str] = []
    for path in sorted(DOCS.glob('11-mobile-*.md')):
        lines = path.read_text(encoding='utf-8').splitlines()
        changed = False
        for index, line in enumerate(lines):
            if not line.startswith('| M'):
                continue
            cells = [cell.strip() for cell in line.strip().strip('|').split('|')]
            if len(cells) != 13:
                raise ValueError(f'{path.name}: {line[:40]}')
            fixed = _fix_cells(cells)
            if fixed == cells:
                continue
            mid = cells[0]
            for lang in LANGS:
                col = _COL[lang]
                if cells[col] != fixed[col]:
                    notes.append(f'{mid} {lang}: «{cells[col]}» → «{fixed[col]}»')
            lines[index] = _render(fixed)
            changed = True
        if changed:
            path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    changelog = _changelog(notes)
    (DOCS / 'CHANGES.md').write_text(changelog, encoding='utf-8')
    return notes


def _changelog(notes: list[str]) -> str:
    body = '\n'.join(f'- {note}' for note in notes) if notes else '- Повторний запуск: тексти вже збігаються з правилами.'
    return f'''# Зміни текстів мобільного довідника

Джерело: `11-mobile-1-ekrany.md`, `11-mobile-2-brendy.md`, `11-mobile-3-yurydychni.md`, `11-mobile-4-interfeis.md`.

Історії брендів M040–M089 не змінювались, окрім прізвища «Турренте» → «Туррент» і фрази «дім брендів» → «дім бренду», якщо вона є. Підпис таба «Дім» (M015) без змін. Позначка 21+ і решта фактів брендів без змін. У перекладах прізвище лишається «Turrent».

Термін дому бренду: українською «дім бренду» / «дому бренду», en «brand house», zh «品牌之家», ms «rumah jenama», fil «bahay ng brand», id «rumah merek», vi «ngôi nhà thương hiệu».

## Правки комірок

{body}
'''


if __name__ == '__main__':
    found = apply()
    print(f'notes: {len(found)}')
    for line in found:
        print(line[:240])
