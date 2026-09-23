from __future__ import annotations

from hashlib import md5
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalog.models import Product, ProductImage, ProductReview

# Demo photos live in static/; seed copies them into MEDIA for ProductImage.
STATIC_PRODUCT_IMAGES = {
    'maduro-robusto': 'pack-01.png',
    'capa-oscura-toro': 'pack-02.png',
    'serie-v-melanio': 'pack-03.png',
    '1880-gran-toro': 'cigar-gran-toro.png',
    '12-years-epicure': 'cigar-epicure.png',
    'reserva-privada': 'cigar-belicoso.png',
    'new-world-dorado': 'cigar-dorado.png',
    'guillotine-classic': 'guillotine.png',
}


WRAPPERS = (
    'Connecticut Shade',
    'Habano Rosado',
    'San Andrés Maduro',
    'Cameroon',
    'Sumatra',
    'Broadleaf Oscuro',
)

BINDERS = (
    'Nicaraguan',
    'Dominican Piloto',
    'Ecuadorian',
    'Mexican San Andrés',
)

FILLERS = (
    'Nicaragua (Estelí, Condega, Jalapa)',
    'Dominican Republic (Piloto, Olor)',
    'Nicaragua + Dominican long filler',
    'Nicaragua Estelí ligero & viso',
)

SMOKE_TIMES = (
    '35–45 хв',
    '45–60 хв',
    '60–75 хв',
    '75–90 хв',
)

NOTES = (
    'Дерево, кедр, легка солодкість, білий перець.',
    'Какао, кава, горіхи, карамель у фіналі.',
    'Шкіра, дуб, какао-боби, приглушений перець.',
    'Кремова текстура, ваніль, кедр, мед.',
    'Прянощі, какао, дуб, мʼяка солодкість.',
)

RECOMMENDATIONS = (
    'Ідеальна для вечірнього ритуалу з single malt або espresso.',
    'Підійде після легкої вечері — не перевантажує смаковий баланс.',
    'Для досвідчених палінь: повільний темп, щоб розкрити складний blend.',
    'Краще з темним шоколадом 70%+ або кавою cold brew.',
    'Рекомендуємо 30–40 хвилин відпочинку в хумідорі перед розкурюванням.',
)

HISTORY_TEMPLATES = (
    '{brand} створила {name} як відповідь на запит колекціонерів на глибший, '
    'більш структурований профіль. Лінія {line} зʼявилася після серії експериментів '
    'на фабриці в {country} — сигара зібрана вручну з відібраним long filler.',
    '{name} — одна з візитівок {brand}. За легендою, рецепт blend уточнювався '
    'кілька сезонів, поки мастер-блендер не зафіксував баланс wrapper і filler '
    'саме для ритуалу Royal Smoke.',
    'Походження {name} сягає традицій {country}: wrapper відбирають за кольором '
    'і еластичністю, а filler — за міцністю горіння. {brand} позиціонує цю позицію '
    'в лінії {line} як «щоденну преміум» сигару.',
)

DESC_TEMPLATES = (
    '{name} — {strength_label} сигара з чітким профілем і рівним горінням. '
    'На першій третині — {note_short}; далі профіль стає глибшим, з тривалим '
    'післясмаком. Зберігання та відбір — у хумідорах Royal Smoke.',
    'У {name} від {brand} акцент на балансі: wrapper задає ароматику, '
    'binder тримає конструкцію, filler — тривалість і міцність ({strength_label}). '
    'Рекомендований темп — один затяг на 30–45 секунд.',
)

REVIEW_TEXTS = (
    'Рівне горіння, без гіркоти. Взяли ще раз у коробку.',
    'Сервіс Royal Smoke як завжди — сигара приїхала в ідеальній вологості.',
    'Для вечора після роботи — саме те. Нотки кави відчуваються чітко.',
    'Порівнював з іншими vitolas цієї лінії — ця мʼякша, але з характером.',
    'Подарункова упаковка не потрібна — сам продукт говорить за себе.',
)

REVIEW_NAMES = (
    'Alexander', 'Michael', 'Irene', 'Dmitry', 'Catherine', 'Andrew', 'Julia',
)


def _seed_int(key: str) -> int:
    return int(md5(key.encode()).hexdigest(), 16)


class Command(BaseCommand):
    help = 'Заповнює картку товару: історія, опис, blend, відео, відгуки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перегенерувати тексти навіть якщо поля вже заповнені',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = bool(options.get('force'))
        products = list(
            Product.objects.filter(is_active=True).select_related('brand', 'line', 'category')
        )
        if not products:
            self.stdout.write(self.style.WARNING('Немає активних товарів'))
            return

        updated_products = 0
        created_images = 0
        created_reviews = 0

        for product in products:
            seed = _seed_int(f'{product.pk}-{product.slug}')
            line_name = product.line.name if product.line else 'Signature'
            strength_label = product.get_strength_display() if product.strength else 'середня'
            note = NOTES[seed % len(NOTES)]
            note_short = note.split(',')[0].strip().lower()

            changed = False

            if force or not product.short_story.strip():
                product.short_story = HISTORY_TEMPLATES[seed % len(HISTORY_TEMPLATES)].format(
                    brand=product.brand.name,
                    name=product.name,
                    line=line_name,
                    country=product.country or product.brand.country or 'Центральної Америки',
                )
                changed = True

            if force or not product.description.strip():
                product.description = DESC_TEMPLATES[seed % len(DESC_TEMPLATES)].format(
                    name=product.name,
                    brand=product.brand.name,
                    strength_label=strength_label,
                    note_short=note_short,
                )
                changed = True

            if force or not product.tasting_notes.strip():
                product.tasting_notes = note
                changed = True

            if force or not product.recommendations.strip():
                product.recommendations = RECOMMENDATIONS[seed % len(RECOMMENDATIONS)]
                changed = True

            if force or not product.wrapper.strip():
                product.wrapper = WRAPPERS[seed % len(WRAPPERS)]
                changed = True

            if force or not product.binder.strip():
                product.binder = BINDERS[(seed // 3) % len(BINDERS)]
                changed = True

            if force or not product.filler.strip():
                product.filler = FILLERS[(seed // 7) % len(FILLERS)]
                changed = True

            if not product.country.strip():
                product.country = product.brand.country or 'Нікарагуа'
                changed = True

            if not product.strength:
                strengths = list(Product.Strength.values)
                product.strength = strengths[seed % len(strengths)]
                changed = True

            if force or not product.smoke_time.strip():
                product.smoke_time = SMOKE_TIMES[seed % len(SMOKE_TIMES)]
                changed = True

            # Do not auto-attach the ambient demo reel to product cards.
            demo = (product.video_url or '').strip()
            if demo.endswith('product-card.mp4') or demo == '/static/video/product-card.mp4':
                product.video_url = ''
                changed = True

            if changed:
                product.save()
                updated_products += 1

            created_images += self._ensure_primary_image(product)
            created_images += self._ensure_gallery(product, seed)
            created_reviews += self._ensure_reviews(product, seed, force)

        self.stdout.write(self.style.SUCCESS(
            f'Готово: {len(products)} товарів, оновлено {updated_products}, '
            f'+{created_images} фото, +{created_reviews} відгуків'
        ))

    def _ensure_primary_image(self, product: Product) -> int:
        if product.images.exists():
            return 0
        filename = STATIC_PRODUCT_IMAGES.get(product.slug, 'pack-01.png')
        path = Path(settings.BASE_DIR) / 'static' / 'img' / 'products' / filename
        if not path.is_file():
            self.stdout.write(self.style.WARNING(f'Немає фото для {product.slug}: {path}'))
            return 0
        img = ProductImage(
            product=product,
            alt_text=product.name,
            sort_order=0,
            is_primary=True,
        )
        with path.open('rb') as fh:
            img.image.save(f'{product.slug}{path.suffix}', File(fh), save=True)
        return 1

    def _ensure_gallery(self, product: Product, seed: int) -> int:
        images = list(product.images.order_by('sort_order', 'id'))
        if len(images) >= 3:
            return 0
        if not images:
            return 0

        primary = images[0]
        created = 0
        labels = (
            f'{product.name} — angle 2',
            f'{product.name} — wrapper details',
            f'{product.name} — cap & band',
        )
        for i in range(3 - len(images)):
            alt = labels[i % len(labels)]
            if ProductImage.objects.filter(product=product, alt_text=alt).exists():
                continue
            dup = ProductImage(
                product=product,
                alt_text=alt,
                sort_order=len(images) + i,
                is_primary=False,
            )
            dup.image = primary.image
            dup.save()
            created += 1
        return created

    def _ensure_reviews(self, product: Product, seed: int, force: bool) -> int:
        published = product.reviews.filter(is_published=True).count()
        if published >= 2 and not force:
            return 0
        if force:
            product.reviews.all().delete()

        created = 0
        for i in range(3):
            author = REVIEW_NAMES[(seed + i) % len(REVIEW_NAMES)]
            rating = 4 + ((seed + i * 3) % 2)
            ProductReview.objects.create(
                product=product,
                author_name=author,
                rating=rating,
                text=REVIEW_TEXTS[(seed + i) % len(REVIEW_TEXTS)],
                is_published=True,
            )
            created += 1
        return created
