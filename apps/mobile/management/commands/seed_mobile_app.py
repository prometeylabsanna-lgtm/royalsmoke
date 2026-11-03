from __future__ import annotations

import sys
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError, no_translations
from django.db import transaction
from modeltranslation.utils import build_localized_fieldname

from apps.mobile.models import (
    MobileBrand,
    MobileBrandFact,
    MobileBrandLine,
    MobileHouseBlock,
    MobileLegalPage,
    MobileScreen,
    MobileSettings,
)

_I18N = Path(__file__).resolve().parents[4] / 'scripts' / 'i18n'
if str(_I18N) not in sys.path:
    sys.path.insert(0, str(_I18N))

from mobile_seed_plan import (  # noqa: E402
    BRANDS,
    HERO,
    HOUSE_BLOCKS,
    LEGAL,
    SCREENS,
    SETTINGS,
    TRANSLATED_BLOCK,
    TRANSLATED_SCREEN,
    TRANSLATED_SETTINGS,
    check_lengths,
)
from mobile_tables import LANGS, by_id  # noqa: E402

MOBILE_ROOT = Path(settings.BASE_DIR) / 'mobile' / 'assets' / 'images'


def _values(phrase) -> dict[str, str]:
    return {code: phrase.text(code) for code in LANGS}


def _assign(obj, field: str, values: dict[str, str]) -> None:
    for code, text in values.items():
        setattr(obj, build_localized_fieldname(field, code), text)
    setattr(obj, field, values['uk'])


def _assign_phrase(obj, field: str, phrase) -> None:
    _assign(obj, field, _values(phrase))


def _sync_rows(existing, count):
    rows = list(existing)
    while len(rows) > count:
        rows.pop().delete()
    return rows


def _attach_image(instance, field_name: str, relative: str) -> bool:
    path = MOBILE_ROOT / relative
    if not path.is_file():
        return False
    field = getattr(instance, field_name)
    if field and field.name:
        return False
    with path.open('rb') as fh:
        field.save(path.name, File(fh), save=True)
    return True


class Command(BaseCommand):
    help = 'Синхронізує тексти мобільного застосунку з таблиць M001–M159. Зображення не перезаписує.'

    @no_translations
    def handle(self, *args, **options):
        rows = by_id()
        errors = check_lengths(rows)
        if errors:
            raise CommandError('Текст довший за поле моделі:\n' + '\n'.join(errors))
        with transaction.atomic():
            self._settings(rows)
            self._brands(rows)
            self._screens(rows)
            self._legal(rows)
        self.stdout.write(self.style.SUCCESS('seed_mobile_app done'))

    def _settings(self, rows) -> None:
        obj = MobileSettings.load()
        for field in TRANSLATED_SETTINGS:
            _assign_phrase(obj, field, rows[SETTINGS[field]])
        if not obj.app_version:
            obj.app_version = rows[SETTINGS['app_version']].text('uk')
        if not obj.contact_phone:
            obj.contact_phone = rows[SETTINGS['contact_phone']].text('uk')
        if not obj.contact_lat:
            obj.contact_lat = 50.4501
        if not obj.contact_lng:
            obj.contact_lng = 30.5226
        obj.save()
        self.stdout.write('settings ok')

    def _brands(self, rows) -> None:
        for index, spec in enumerate(BRANDS):
            name = rows[spec['name']].text('uk')
            brand, created = MobileBrand.objects.get_or_create(
                slug=spec['slug'],
                defaults={'name': name, 'sort_order': index},
            )
            brand.name = name
            brand.short_name = rows[spec['short_name']].text('uk')
            brand.mono = rows[spec['mono']].text('uk')
            brand.panel = spec['panel']
            brand.sort_order = index
            _assign_phrase(brand, 'country', rows[spec['country']])
            _assign_phrase(brand, 'heritage', rows[spec['heritage']])
            brand.save()
            _attach_image(brand, 'cover', spec['cover'])
            facts = _sync_rows(brand.facts.order_by('sort_order', 'id'), len(spec['facts']))
            for fact_index, (label_id, value_id) in enumerate(spec['facts']):
                fact = facts[fact_index] if fact_index < len(facts) else MobileBrandFact(brand=brand)
                _assign_phrase(fact, 'label', rows[label_id])
                _assign_phrase(fact, 'value', rows[value_id])
                fact.sort_order = fact_index
                fact.save()
            lines = _sync_rows(brand.lines.order_by('sort_order', 'id'), len(spec['lines']))
            for line_index, line_id in enumerate(spec['lines']):
                line = lines[line_index] if line_index < len(lines) else MobileBrandLine(brand=brand)
                line.name = rows[line_id].text('uk')
                line.sort_order = line_index
                line.save()
            self.stdout.write(f'brand {brand.slug} {"created" if created else "updated"}')

    def _screens(self, rows) -> None:
        for key, spec in SCREENS.items():
            screen, created = MobileScreen.objects.get_or_create(key=key)
            for field in TRANSLATED_SCREEN:
                if field in spec:
                    _assign_phrase(screen, field, rows[spec[field]])
                else:
                    _assign(screen, field, {code: '' for code in LANGS})
            screen.save()
            hero = HERO.get(key)
            if hero:
                _attach_image(screen, 'hero_image', hero)
            if key == 'house':
                blocks = _sync_rows(
                    screen.house_blocks.order_by('sort_order', 'id'),
                    len(HOUSE_BLOCKS),
                )
                for block_index, (index_id, title_id, body_id) in enumerate(HOUSE_BLOCKS):
                    block = blocks[block_index] if block_index < len(blocks) else MobileHouseBlock(screen=screen)
                    block.index_label = rows[index_id].text('uk')
                    for field, phrase_id in zip(TRANSLATED_BLOCK, (title_id, body_id), strict=True):
                        _assign_phrase(block, field, rows[phrase_id])
                    block.sort_order = block_index
                    block.save()
            self.stdout.write(f'screen {key} {"created" if created else "updated"}')

    def _legal(self, rows) -> None:
        for slug, spec in LEGAL.items():
            title = rows[spec['title']]
            body_ids = spec['body']
            body_uk = '\n\n'.join(rows[item].text('uk') for item in body_ids)
            page, created = MobileLegalPage.objects.get_or_create(
                slug=slug,
                defaults={'title': title.text('uk'), 'body': body_uk},
            )
            _assign_phrase(page, 'title', title)
            _assign(
                page,
                'body',
                {code: '\n\n'.join(rows[item].text(code) for item in body_ids) for code in LANGS},
            )
            page.save()
            self.stdout.write(f'page {slug} {"created" if created else "updated"}')
