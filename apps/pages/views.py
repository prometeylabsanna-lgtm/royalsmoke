from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from apps.catalog.models import Brand, Product
from apps.core.block_defaults import BLOCK_DEFAULTS, HISTORY_SLIDE_DEFAULTS
from apps.core.models import HeroSlide, HistorySlide, HomeBrandCard, SiteBlock, SiteSettings


def _block(page: str, key: str) -> str:
    b = SiteBlock.objects.filter(page=page, key=key, is_active=True).first()
    if b and b.text_html:
        return b.text_html
    return BLOCK_DEFAULTS.get((page, key), '')


def _block_image(page: str, key: str):
    b = SiteBlock.objects.filter(page=page, key=key, is_active=True).first()
    if b and b.image:
        return b.image
    return None


def _fallback_history_slides():
    from types import SimpleNamespace
    return [SimpleNamespace(**item, is_active=True) for item in HISTORY_SLIDE_DEFAULTS]


def _enrich_history_slides(slides):
    from apps.core.block_defaults import HISTORY_IMAGE_FALLBACKS

    enriched = []
    for i, slide in enumerate(slides):
        if not getattr(slide, 'image', None):
            slide.image_static = HISTORY_IMAGE_FALLBACKS[i % len(HISTORY_IMAGE_FALLBACKS)]
        enriched.append(slide)
    return enriched


_BRAND_CRAFT_TONES = ('amber', 'burgundy', 'green', 'brown')


def _brand_static_image(brand) -> str:
    from apps.core.block_defaults import BRAND_IMAGE_FALLBACKS

    return BRAND_IMAGE_FALLBACKS.get(getattr(brand, 'slug', '') or '', '')


def _enrich_brand_craft(brands):
    enriched = []
    for i, brand in enumerate(brands[:4]):
        logo = ''
        if getattr(brand, 'logo', None):
            try:
                logo = brand.logo.url
            except ValueError:
                logo = ''
        desc = (brand.short_description or brand.description or '').strip()
        enriched.append({
            'brand': brand,
            'tone': _BRAND_CRAFT_TONES[i % len(_BRAND_CRAFT_TONES)],
            'image': logo,
            'image_static': '' if logo else _brand_static_image(brand),
            'description': desc,
            'flip': i % 2 == 1,
        })
    return enriched


def _home_brand_cards():
    from apps.core.block_defaults import BRAND_CARD_TEXT_DEFAULTS

    cards = list(
        HomeBrandCard.objects.filter(is_active=True, brand__is_active=True)
        .select_related('brand')
        .order_by('sort_order', 'id')
    )
    if not cards:
        return None
    enriched = []
    for i, card in enumerate(cards):
        image = ''
        if card.image:
            try:
                image = card.image.url
            except ValueError:
                image = ''
        if not image and card.brand.logo:
            try:
                image = card.brand.logo.url
            except ValueError:
                image = ''
        desc = (card.text or card.brand.short_description or card.brand.description or '').strip()
        if not desc:
            desc = BRAND_CARD_TEXT_DEFAULTS.get(card.brand.slug, '')
        enriched.append({
            'brand': card.brand,
            'tone': _BRAND_CRAFT_TONES[i % len(_BRAND_CRAFT_TONES)],
            'image': image,
            'image_static': '' if image else _brand_static_image(card.brand),
            'description': desc,
            'flip': i % 2 == 1,
        })
    return enriched


def home(request):
    SiteSettings.load()
    products = Product.objects.on_storefront().with_relations().order_by('sort_order', 'name')[:6]
    brand_craft = _home_brand_cards()
    if brand_craft is None:
        brands = list(
            Brand.objects.filter(is_active=True, is_featured=True).order_by('sort_order', 'name')[:4]
        )
        if not brands:
            brands = list(
                Brand.objects.filter(is_active=True).order_by('sort_order', 'name')[:4]
            )
        brand_craft = _enrich_brand_craft(brands)
    else:
        brands = [item['brand'] for item in brand_craft]
    slides = list(HeroSlide.objects.filter(is_active=True))
    history_slides = list(HistorySlide.objects.filter(is_active=True))
    if not history_slides:
        history_slides = _fallback_history_slides()
    history_slides = _enrich_history_slides(history_slides)
    return render(request, 'pages/home.html', {
        'home_products': products,
        'brands': brands,
        'brand_craft': brand_craft,
        'hero_slides': slides,
        'history_slides': history_slides,
        'history_kicker': _block('home', 'about_kicker') or _('Історія'),
        'history_bg': _block_image('home', 'about_bg'),
    })


def about(request):
    return render(request, 'pages/about.html')


def faq(request):
    from apps.pages.models import FAQItem
    return render(request, 'pages/faq.html', {
        'faq_items': FAQItem.objects.filter(is_active=True),
    })


def legal(request, slug='privacy'):
    from django.shortcuts import get_object_or_404

    from apps.pages.models import LegalDocument

    doc = get_object_or_404(LegalDocument, slug=slug, is_active=True)
    return render(request, 'pages/legal.html', {
        'doc': doc,
        'legal_docs': LegalDocument.objects.filter(is_active=True),
        'slug': slug,
    })


@require_POST
def age_gate_set(request):
    allowed = request.POST.get('allowed') == '1'
    response = HttpResponse(status=204)
    max_age = 60 * 60 * 24 * 30
    response.set_cookie(
        'age_ok',
        '1' if allowed else '0',
        max_age=max_age,
        samesite='Lax',
        httponly=False,
        secure=request.is_secure(),
    )
    return response
