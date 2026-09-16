from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_POST

from apps.catalog.models import Brand, Product
from apps.core.block_defaults import BLOCK_DEFAULTS, HISTORY_SLIDE_DEFAULTS
from apps.core.models import HeroSlide, HistorySlide, SiteBlock, SiteSettings


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


_BRAND_CRAFT_TONES = (
    {
        'tone': 'amber',
        'image': (
            'https://images.unsplash.com/photo-1741306444151-ec7f9ac433ef'
            '?auto=format&fit=crop&w=1400&q=80'
        ),
        'fallback': gettext_lazy(
            'Нікарагуанська школа майстерності: насичений смак, щільна скрутка '
            'та характерний maduro. Сигари AJ Fernandez — для тих, хто цінує '
            'глибину профілю, довгий фініш і ритуал повільного куріння.'
        ),
    },
    {
        'tone': 'burgundy',
        'image': (
            'https://images.unsplash.com/photo-1631227852854-7c0fac3c9aeb'
            '?auto=format&fit=crop&w=1400&q=80'
        ),
        'fallback': gettext_lazy(
            'Глибокі профілі з нотами какао, шкіри та кедру — Oliva створює '
            'сигари для довгого вечірнього ритуалу. Баланс сили й елегантності, '
            'витриманий тютюн і бездоганна скрутка.'
        ),
    },
    {
        'tone': 'green',
        'image': (
            'https://images.unsplash.com/photo-1749842839766-8b71630a627d'
            '?auto=format&fit=crop&w=1400&q=80'
        ),
        'fallback': gettext_lazy(
            'Свіжі ноти тютюнового листа, акуратна ферментація та чистий фініш. '
            'Perdomo — сімейна традиція, де кожна сигара проходить відбір '
            'і контроль вологості для ідеального куріння.'
        ),
    },
    {
        'tone': 'brown',
        'image': (
            'https://images.unsplash.com/photo-1686704176261-a77939eb0f7c'
            '?auto=format&fit=crop&w=1400&q=80'
        ),
        'fallback': gettext_lazy(
            'Земляні тони мексиканського terroir, деревʼяна коробка та аксесуари '
            'для повільного ритуалу. Casa Turrent поєднує історію родини '
            'з сучасним характером преміальної сигари.'
        ),
    },
)


def _enrich_brand_craft(brands):
    """Attach tone / Unsplash image / copy for home craft section (max 4)."""
    enriched = []
    for i, brand in enumerate(brands[:4]):
        meta = _BRAND_CRAFT_TONES[i % len(_BRAND_CRAFT_TONES)]
        raw = (brand.short_description or brand.description or '').strip()
        if len(raw) < 80:
            desc = meta['fallback']
            if raw:
                desc = raw.rstrip('.') + '. ' + meta['fallback']
        else:
            desc = raw
        enriched.append({
            'brand': brand,
            'tone': meta['tone'],
            'image': meta['image'],
            'description': desc,
            'flip': i % 2 == 1,
        })
    return enriched


def home(request):
    SiteSettings.load()
    products = Product.objects.on_storefront().with_relations().order_by('sort_order', 'name')[:6]
    brands = list(
        Brand.objects.filter(is_active=True, is_featured=True).order_by('sort_order', 'name')[:4]
    )
    if not brands:
        brands = list(
            Brand.objects.filter(is_active=True).order_by('sort_order', 'name')[:4]
        )
    brand_craft = _enrich_brand_craft(brands)
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
    return render(request, 'pages/faq.html')


def legal(request, slug='privacy'):
    return render(request, 'pages/legal.html', {'slug': slug})


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
