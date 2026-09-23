from __future__ import annotations

from django.conf import settings
from django.utils import timezone
from django.utils.translation import activate, get_language

from apps.catalog.models import Brand, Category, Product
from apps.core.currency import convert_from_uah, get_currency, language_currency_code


def _img_url(field) -> str:
    if not field:
        return ''
    try:
        return field.url
    except ValueError:
        return ''


def _product_image(product: Product) -> str:
    images = list(product.images.all())
    if not images:
        return ''
    primary = next((i for i in images if i.is_primary), None) or images[0]
    return _img_url(primary.image)


def _lang_codes() -> list[str]:
    return [code for code, _ in getattr(settings, 'LANGUAGES', [('uk', 'UK')])]


def build_catalog_snapshot() -> dict:
    """Full active catalog for offline PWA, all storefront languages."""
    products_qs = (
        Product.objects.on_storefront()
        .with_relations()
        .prefetch_related('images')
        .order_by('sort_order', 'name', 'id')
    )
    categories_qs = Category.objects.filter(is_active=True).order_by('sort_order', 'name')
    brands_qs = Brand.objects.filter(is_active=True).order_by('sort_order', 'name')

    # Materialize once; translated fields resolved per activate().
    products = list(products_qs)
    categories = list(categories_qs)
    brands = list(brands_qs)

    prev = get_language()
    langs: dict[str, dict] = {}
    try:
        for lang in _lang_codes():
            activate(lang)
            cur = get_currency(language_currency_code(lang))
            langs[lang] = {
                'currency': {
                    'code': cur['code'],
                    'symbol': cur.get('symbol') or cur['code'],
                },
                'categories': [
                    {
                        'slug': c.slug,
                        'name': c.name,
                        'kind': c.kind,
                        'description': c.description or '',
                        'url': c.get_absolute_url(),
                        'image': _img_url(c.image),
                    }
                    for c in categories
                ],
                'brands': [
                    {
                        'slug': b.slug,
                        'name': b.name,
                        'country': b.country or '',
                        'short_description': b.short_description or '',
                        'description': b.description or '',
                        'url': b.get_absolute_url(),
                        'logo': _img_url(b.logo),
                    }
                    for b in brands
                ],
                'products': [
                    {
                        'slug': p.slug,
                        'name': p.name,
                        'sku': p.sku or '',
                        'url': p.get_absolute_url(),
                        'brand_slug': p.brand.slug if p.brand_id else '',
                        'brand_name': p.brand.name if p.brand_id else '',
                        'category_slug': p.category.slug if p.category_id else '',
                        'category_name': p.category.name if p.category_id else '',
                        'short_story': p.short_story or '',
                        'description': p.description or '',
                        'tasting_notes': p.tasting_notes or '',
                        'wrapper': p.wrapper or '',
                        'binder': p.binder or '',
                        'filler': p.filler or '',
                        'country': p.country or '',
                        'strength': p.strength or '',
                        'smoke_time': p.smoke_time or '',
                        'price': str(convert_from_uah(p.base_price, cur['code'])),
                        'old_price': (
                            str(convert_from_uah(p.old_price, cur['code']))
                            if p.old_price is not None
                            else None
                        ),
                        'stock': int(p.stock or 0),
                        'image': _product_image(p),
                        'updated_at': p.updated_at.isoformat() if p.updated_at else '',
                    }
                    for p in products
                ],
            }
    finally:
        if prev:
            activate(prev)

    return {
        'version': 1,
        'generated_at': timezone.now().isoformat(),
        'langs': langs,
    }
