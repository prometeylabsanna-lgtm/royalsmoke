from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.booking.models import BookingService, BookingSlot
from apps.calculator.models import CalculatorOption, CalculatorQuestion
from apps.catalog.models import Product, ProductVariant
from apps.catalog.models_base import Brand, Category, ProductLine, Tag
from apps.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    BLOCK_FIELD_LABELS,
    FAQ_ITEM_DEFAULTS,
    HISTORY_SLIDE_DEFAULTS,
    LEGAL_DOC_DEFAULTS,
)
from apps.core.models import HeroSlide, HistorySlide, HomeBrandCard, SiteBlock, SiteSettings
from apps.core.page_styles import ensure_page_styles
from apps.core.delivery_cards import ensure_delivery_cards


class Command(BaseCommand):
    help = 'Ідемпотентний seed: CMS-блоки, демо-каталог, калькулятор, бронювання'

    def handle(self, *args, **options):
        SiteSettings.load()
        ensure_page_styles()
        ensure_delivery_cards()
        self._seed_blocks()
        self._seed_hero()
        self._seed_history()
        self._seed_catalog()
        self._seed_brand_cards()
        self._seed_page_bg_images()
        self._seed_faq()
        self._seed_legal()
        self._seed_calculator()
        self._seed_booking()
        self.stdout.write(self.style.SUCCESS('Seed завершено'))

    def _seed_blocks(self):
        force_keys = {
            ('service', 'booking_lead'),
        }
        booking_lead_uk = str(BLOCK_DEFAULTS[('service', 'booking_lead')])
        booking_lead_en = (
            'Leave your contacts — a manager will arrange a convenient visit time.\n\n'
            'We will call back during business hours to confirm the slot and answer questions.\n\n'
            'Choose a tasting, sommelier consultation, or a quiet showroom visit — we adapt to your pace.'
        )
        booking_lead_zh = (
            '留下联系方式——经理将安排方便的参观时间。\n\n'
            '我们会在工作日内回电确认时段并解答疑问。\n\n'
            '可选品鉴、侍茄师咨询或安静的展厅到访——我们按您的节奏安排。'
        )

        for (page, key), text in BLOCK_DEFAULTS.items():
            defaults = {
                'label': BLOCK_FIELD_LABELS.get((page, key), key),
                'content_type': BLOCK_CONTENT_TYPES.get((page, key), 'text'),
                'text_html': str(text),
                'is_active': True,
            }
            block, created = SiteBlock.objects.get_or_create(
                page=page,
                key=key,
                defaults=defaults,
            )
            if created or (page, key) not in force_keys:
                continue
            block.text_html = booking_lead_uk
            block.text_html_uk = booking_lead_uk
            block.text_html_en = booking_lead_en
            block.text_html_zh_hans = booking_lead_zh
            block.is_active = True
            block.save()

    def _seed_hero(self):
        from pathlib import Path

        from django.conf import settings
        from django.core.files import File

        from apps.core.block_defaults import HERO_IMAGE_FALLBACKS

        if not HeroSlide.objects.exists():
            slides = [
                (
                    'Сигари, відібрані вручну для тих, хто знає різницю',
                    'Понад 400 позицій з мануфактур Нікарагуа, Домінікани та Куби.',
                ),
                (
                    'Лімітовані лінії AJ Fernandez уже в наявності',
                    'Bellas Artes, New World, Enclave — повні вітоли та подарункові набори.',
                ),
                (
                    'Аксесуари, які тримають ритуал',
                    'Хумідори, гільйотини, попільниці та футляри від європейських майстерень.',
                ),
            ]
            for i, (title, sub) in enumerate(slides):
                HeroSlide.objects.create(
                    title=title, subtitle=sub, sort_order=i, is_active=True,
                )

        static_root = Path(settings.BASE_DIR) / 'static'
        for i, slide in enumerate(HeroSlide.objects.order_by('sort_order', 'id')):
            if slide.image:
                continue
            rel = HERO_IMAGE_FALLBACKS[i % len(HERO_IMAGE_FALLBACKS)]
            path = static_root / rel
            if not path.is_file():
                continue
            with path.open('rb') as fh:
                slide.image.save(path.name, File(fh), save=True)

    def _seed_history(self):
        from pathlib import Path

        from django.conf import settings
        from django.core.files import File

        from apps.core.block_defaults import HISTORY_IMAGE_FALLBACKS

        if not HistorySlide.objects.exists():
            for item in HISTORY_SLIDE_DEFAULTS:
                HistorySlide.objects.create(
                    year_label=item['year_label'],
                    title=item['title'],
                    text=item['text'],
                    cta_label=item.get('cta_label') or '',
                    cta_url=item.get('cta_url') or '',
                    sort_order=item['sort_order'],
                    is_active=True,
                )

        HistorySlide.objects.filter(is_active=True).update(cta_label='', cta_url='')

        static_root = Path(settings.BASE_DIR) / 'static'
        for slide in HistorySlide.objects.filter(is_active=True).order_by('sort_order', 'id'):
            rel = HISTORY_IMAGE_FALLBACKS[slide.sort_order % len(HISTORY_IMAGE_FALLBACKS)]
            path = static_root / rel
            if not path.is_file():
                continue
            with path.open('rb') as fh:
                slide.image.save(path.name, File(fh), save=True)

    def _seed_catalog(self):
        Tag.objects.get_or_create(slug='top', defaults={'name': 'Топ продажів'})
        Tag.objects.get_or_create(slug='new', defaults={'name': 'Новинки'})
        top = Tag.objects.get(slug='top')
        new = Tag.objects.get(slug='new')

        cats = [
            ('Сигари', 'cigars', Category.Kind.CIGARS, True),
            ('Аксесуари', 'accessories', Category.Kind.ACCESSORIES, True),
            ('Сигарети', 'cigarettes', Category.Kind.CIGARETTES, False),
        ]
        cat_map = {}
        for name, slug, kind, featured in cats:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name, 'kind': kind, 'is_featured': featured, 'is_active': True,
                },
            )
            cat_map[slug] = cat

        brands_data = [
            ('AJ Fernandez', 'aj-fernandez', 'Нікарагуа', True, 0),
            ('Oliva', 'oliva', 'Нікарагуа', True, 1),
            ('Perdomo', 'perdomo', 'Нікарагуа', True, 2),
            ('Casa Turrent', 'casa-turrent', 'Мексика', True, 3),
            ('PDR Cigars', 'pdr-cigars', 'Домінікана', False, 4),
            ('Quesada', 'quesada', 'Домінікана', False, 5),
        ]
        brand_map = {}
        for name, slug, country, featured, order in brands_data:
            b, _ = Brand.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name, 'country': country, 'is_active': True,
                    'is_featured': featured, 'sort_order': order,
                },
            )
            changed = False
            if b.is_featured != featured:
                b.is_featured = featured
                changed = True
            if b.sort_order != order:
                b.sort_order = order
                changed = True
            if changed:
                b.save(update_fields=['is_featured', 'sort_order'])
            brand_map[slug] = b

        if Product.objects.exists():
            return

        demo = [
            ('aj-fernandez', 'cigars', 'Maduro Robusto', 'maduro-robusto', 'medium', '1240', 'Robusto', True, False),
            ('pdr-cigars', 'cigars', 'Capa Oscura Toro', 'capa-oscura-toro', 'medium_full', '980', 'Toro', True, False),
            ('oliva', 'cigars', 'Serie V Melanio', 'serie-v-melanio', 'full', '2150', 'Figurado', True, False),
            ('casa-turrent', 'cigars', '1880 Gran Toro', '1880-gran-toro', 'medium', '1890', 'Gran Toro', True, False),
            ('perdomo', 'cigars', '12 Years Epicure', '12-years-epicure', 'medium', '1420', 'Epicure', False, True),
            ('quesada', 'cigars', 'Reserva Privada Belicoso', 'reserva-privada', 'medium_full', '1680', 'Belicoso', False, True),
            ('aj-fernandez', 'cigars', 'New World Dorado', 'new-world-dorado', 'mild', '890', 'Robusto', False, True),
            ('oliva', 'accessories', 'Гільйотина Classic', 'guillotine-classic', '', '1450', '', False, True),
        ]
        for brand_slug, cat_slug, name, slug, strength, price, vitola, is_top, is_new in demo:
            brand = brand_map[brand_slug]
            line, _ = ProductLine.objects.get_or_create(
                slug=f'{brand_slug}-core',
                defaults={'brand': brand, 'name': 'Core', 'is_active': True},
            )
            p = Product.objects.create(
                brand=brand,
                category=cat_map[cat_slug],
                line=line,
                name=name,
                slug=slug,
                short_story=f'{brand.name} — {name}. Відібрано для Royal Smoke.',
                description=f'Детальний опис {name}. Зберігання у власних хумідорах.',
                tasting_notes='Дерево, кава, шкіра',
                wrapper='Habano',
                binder='Nicaraguan',
                filler='Nicaraguan',
                country=brand.country,
                strength=strength or Product.Strength.MEDIUM,
                smoke_time='45–60 хв',
                base_price=Decimal(price),
                stock=20,
                is_active=True,
                is_featured=is_top,
            )
            if vitola:
                ProductVariant.objects.create(
                    product=p,
                    name=vitola,
                    slug=vitola.lower().replace(' ', '-'),
                    length_mm=127,
                    ring_gauge=50,
                    shape=vitola,
                    price=Decimal(price),
                    stock=15,
                    is_active=True,
                )
                ProductVariant.objects.create(
                    product=p,
                    name=f'{vitola} Box',
                    slug=f'{vitola.lower().replace(" ", "-")}-box',
                    length_mm=127,
                    ring_gauge=50,
                    shape=vitola,
                    price=Decimal(price) * 20,
                    stock=3,
                    is_active=True,
                )
            if is_top:
                p.tags.add(top)
            if is_new:
                p.tags.add(new)

    def _seed_calculator(self):
        steps = [
            ('strength', 'Міцність', 1, [
                ('Легка', 'mild', 'strength', 'mild'),
                ('Середня', 'medium', 'strength', 'medium'),
                ('Середньо-повна', 'medium_full', 'strength', 'medium_full'),
                ('Повна', 'full', 'strength', 'full'),
            ]),
            ('format', 'Формат', 2, [
                ('Petit Robusto', 'petit', 'shape', 'Petit'),
                ('Robusto', 'robusto', 'shape', 'Robusto'),
                ('Toro', 'toro', 'shape', 'Toro'),
                ('Churchill', 'churchill', 'shape', 'Churchill'),
            ]),
            ('country', 'Країна', 3, [
                ('Куба', 'cuba', 'country', 'Куба'),
                ('Нікарагуа', 'nicaragua', 'country', 'Нікарагуа'),
                ('Домінікана', 'dominican', 'country', 'Домінікана'),
                ('Будь-яка', '', 'country', ''),
            ]),
            ('budget', 'Бюджет', 4, [
                ('до 1000 ₴', '0-1000', 'budget_range', '0-1000'),
                ('1000—2000 ₴', '1000-2000', 'budget_range', '1000-2000'),
                ('2000—3500 ₴', '2000-3500', 'budget_range', '2000-3500'),
                ('без обмежень', 'any', 'budget_range', 'any'),
            ]),
        ]
        for step_key, title, order, options in steps:
            q, _ = CalculatorQuestion.objects.get_or_create(
                step_key=step_key,
                defaults={'title': title, 'sort_order': order, 'is_active': True},
            )
            # оновлюємо опції під актуальний UI (ідемпотентно)
            existing = {o.value: o for o in q.options.all()}
            keep_values = set()
            for i, (label, value, field, fval) in enumerate(options):
                keep_values.add(value)
                opt = existing.get(value)
                if opt:
                    changed = False
                    for attr, val in (
                        ('label', label),
                        ('filter_field', field),
                        ('filter_value', fval),
                        ('sort_order', i),
                        ('is_active', True),
                    ):
                        if getattr(opt, attr) != val:
                            setattr(opt, attr, val)
                            changed = True
                    if changed:
                        opt.save()
                else:
                    CalculatorOption.objects.create(
                        question=q, label=label, value=value,
                        filter_field=field, filter_value=fval,
                        sort_order=i, is_active=True,
                    )
            q.options.exclude(value__in=keep_values).update(is_active=False)

    def _seed_booking(self):
        services = [
            (BookingService.Kind.TASTING, 'Дегустація', 90, 6),
            (BookingService.Kind.CONSULTATION, 'Консультація сомельє', 45, 1),
            (BookingService.Kind.SHOWROOM, 'Візит у шоурум', 60, 4),
            (BookingService.Kind.PICKUP, 'Самовивіз', 20, 8),
        ]
        start = timezone.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=1)
        for kind, title, duration, capacity in services:
            svc, created = BookingService.objects.get_or_create(
                kind=kind,
                defaults={
                    'title': title, 'duration_minutes': duration,
                    'capacity': capacity, 'is_active': True,
                },
            )
            if not created and svc.slots.exists():
                continue
            for day in range(5):
                for hour in (12, 15, 18):
                    begins = start + timedelta(days=day, hours=hour - start.hour)
                    BookingSlot.objects.get_or_create(
                        service=svc,
                        starts_at=begins,
                        defaults={
                            'ends_at': begins + timedelta(minutes=duration),
                            'capacity': capacity,
                            'is_active': True,
                        },
                    )

    def _seed_brand_cards(self):
        from pathlib import Path

        from django.conf import settings
        from django.core.files import File

        from apps.catalog.models_base import Brand
        from apps.core.block_defaults import BRAND_CARD_TEXT_DEFAULTS, BRAND_IMAGE_FALLBACKS

        brands = list(Brand.objects.filter(is_featured=True).order_by('sort_order', 'id')[:4])
        if not brands:
            brands = list(Brand.objects.filter(is_active=True).order_by('sort_order', 'id')[:4])
        static_root = Path(settings.BASE_DIR) / 'static'
        for i, brand in enumerate(brands):
            text = BRAND_CARD_TEXT_DEFAULTS.get(brand.slug, '')
            if not (brand.short_description or '').strip() and text:
                brand.short_description = text
                brand.save(update_fields=['short_description'])
            card, _ = HomeBrandCard.objects.get_or_create(
                brand=brand,
                defaults={'sort_order': i, 'is_active': True, 'text': text},
            )
            changed = False
            if not (card.text or '').strip() and text:
                card.text = text
                changed = True
            if card.sort_order != i:
                card.sort_order = i
                changed = True
            if not card.is_active:
                card.is_active = True
                changed = True
            if changed:
                card.save(update_fields=['text', 'sort_order', 'is_active'])
            rel = BRAND_IMAGE_FALLBACKS.get(brand.slug)
            if not rel:
                continue
            path = static_root / rel
            if not path.is_file():
                continue
            with path.open('rb') as fh:
                card.image.save(path.name, File(fh), save=True)

    def _seed_page_bg_images(self):
        from pathlib import Path

        from django.conf import settings
        from django.core.files import File

        from apps.core.block_defaults import PAGE_BG_IMAGE_FALLBACKS

        static_root = Path(settings.BASE_DIR) / 'static'
        for (page, key), rel in PAGE_BG_IMAGE_FALLBACKS.items():
            block = SiteBlock.objects.filter(page=page, key=key).first()
            if not block:
                continue
            has_file = False
            if block.image:
                try:
                    has_file = Path(block.image.path).is_file()
                except (ValueError, FileNotFoundError, OSError):
                    has_file = False
            if has_file:
                continue
            path = static_root / rel
            if not path.is_file():
                continue
            with path.open('rb') as fh:
                block.image.save(path.name, File(fh), save=True)

    def _seed_faq(self):
        from apps.pages.models import FAQItem
        if FAQItem.objects.exists():
            return
        for i, item in enumerate(FAQ_ITEM_DEFAULTS):
            FAQItem.objects.create(
                question=item['question'],
                answer=item['answer'],
                sort_order=i,
                is_active=True,
            )

    def _seed_legal(self):
        from apps.core.legal_privacy_body import (
            PRIVACY_BODY_EN,
            PRIVACY_BODY_UK,
            PRIVACY_BODY_ZH,
        )
        from apps.pages.models import LegalDocument

        for i, item in enumerate(LEGAL_DOC_DEFAULTS):
            doc, created = LegalDocument.objects.get_or_create(
                slug=item['slug'],
                defaults={
                    'title': item['title'],
                    'body': item['body'],
                    'sort_order': i,
                    'is_active': True,
                },
            )
            updates: list[str] = []
            if not doc.is_active:
                doc.is_active = True
                updates.append('is_active')
            if not (doc.title or '').strip():
                doc.title = item['title']
                updates.append('title')
            if doc.sort_order != i:
                doc.sort_order = i
                updates.append('sort_order')

            if item['slug'] == 'privacy':
                doc.title = item['title']
                doc.title_uk = item['title']
                doc.title_en = 'Privacy policy'
                doc.title_zh_hans = '隐私政策'
                doc.body = PRIVACY_BODY_UK
                doc.body_uk = PRIVACY_BODY_UK
                doc.body_en = PRIVACY_BODY_EN
                doc.body_zh_hans = PRIVACY_BODY_ZH
                updates.extend([
                    'title', 'title_uk', 'title_en', 'title_zh_hans',
                    'body', 'body_uk', 'body_en', 'body_zh_hans',
                ])
            elif not (doc.body or '').strip():
                doc.body = item['body']
                updates.append('body')

            if updates:
                doc.save(update_fields=list(dict.fromkeys(updates)))

