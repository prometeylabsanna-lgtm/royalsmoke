from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from apps.catalog import compare as compare_services
from apps.catalog.models import Product


_YT_ID_RE = re.compile(
    r'(?:youtu\.be/|youtube\.com/(?:embed/|shorts/|watch\?.*?v=))([A-Za-z0-9_-]{6,})',
)


def youtube_embed_url(url: str) -> str:
    """Return embeddable YouTube URL or empty string."""
    raw = (url or '').strip()
    if not raw:
        return ''
    m = _YT_ID_RE.search(raw)
    if m:
        return f'https://www.youtube.com/embed/{m.group(1)}?rel=0&playsinline=1'
    parsed = urlparse(raw)
    if 'youtube.com' in (parsed.netloc or '') and parsed.path.startswith('/embed/'):
        return raw
    qs = parse_qs(parsed.query or '')
    if qs.get('v'):
        return f'https://www.youtube.com/embed/{qs["v"][0]}?rel=0&playsinline=1'
    return ''


def is_direct_video(url: str) -> bool:
    raw = (url or '').strip().lower()
    return bool(raw) and (
        raw.endswith('.mp4')
        or raw.endswith('.webm')
        or raw.endswith('.ogg')
        or '/static/video/' in raw
        or '/media/' in raw
    )


def related_products(product: Product, limit: int = 4):
    qs = Product.objects.on_storefront().with_relations().exclude(pk=product.pk)
    if product.line_id:
        line_qs = list(qs.filter(line_id=product.line_id)[:limit])
        if line_qs:
            return line_qs
    return list(qs.filter(brand_id=product.brand_id)[:limit])


@require_POST
def compare_toggle(request):
    try:
        product_id = int(request.POST.get('product_id', 0))
    except (TypeError, ValueError):
        product_id = 0
    if product_id:
        compare_services.toggle(request, product_id)

    if not request.htmx:
        return redirect('catalog:compare')

    target = request.htmx.target or ''
    products = compare_services.items(request)
    ids = compare_services.product_ids(request)
    badge = render_to_string(
        'catalog/partials/compare_badge.html',
        {'compare_count': compare_services.count(request), 'oob': True},
        request=request,
    )

    if target == 'compare-body':
        body = render_to_string(
            'catalog/partials/compare_body.html',
            {'products': products, 'compare_count': len(products)},
            request=request,
        )
        return HttpResponse(body + badge)

    product = Product.objects.filter(pk=product_id).first()
    if product:
        btn = render_to_string(
            'catalog/partials/compare_btn.html',
            {'product': product, 'compare_ids': ids},
            request=request,
        )
        return HttpResponse(btn + badge)

    return HttpResponse(badge)


def compare_detail(request):
    products = compare_services.items(request)
    return render(request, 'catalog/compare.html', {
        'products': products,
        'compare_count': len(products),
        'compare_max': compare_services.COMPARE_MAX,
    })
