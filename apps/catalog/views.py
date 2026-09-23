from django.db.models import Prefetch
from django.db import DatabaseError
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from apps.catalog.browser_filters import (
    apply_category_params,
    apply_filters,
    build_browser_context,
)
from apps.catalog.models import Brand, Category, Product, ProductReview
from apps.catalog.pagination import paginate_catalog
from apps.catalog.search import SUGGEST_MIN_LEN, product_search_q, sanitize_search_query
from apps.catalog.views_compare import (
    compare_detail,
    compare_toggle,
    is_direct_video,
    related_products,
    youtube_embed_url,
)

__all__ = [
    'brand_detail',
    'catalog_list',
    'compare_detail',
    'compare_toggle',
    'product_detail',
    'search_suggest',
]


def _catalog_page(request, qs, *, category=None, brand=None):
    products, page_obj = paginate_catalog(qs, request.GET.get('page'))
    ctx = build_browser_context(
        request,
        products=products,
        category=category,
        brand=brand,
        page_obj=page_obj,
    )
    if request.htmx:
        return render(request, 'catalog/partials/product_grid.html', ctx)
    return render(request, 'catalog/list.html', ctx)


def catalog_list(request, slug=None):
    qs = Product.objects.on_storefront().with_relations()
    category = None
    if slug:
        category = get_object_or_404(Category, slug=slug, is_active=True)
    qs = apply_category_params(qs, request.GET, path_category=category)
    qs = apply_filters(qs, request.GET)
    return _catalog_page(request, qs, category=category)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    qs = Product.objects.on_storefront().with_relations().filter(brand=brand)
    qs = apply_category_params(qs, request.GET, path_category=None)
    qs = apply_filters(qs, request.GET)
    return _catalog_page(request, qs, brand=brand)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.on_storefront()
        .with_relations()
        .prefetch_related(
            Prefetch(
                'reviews',
                queryset=ProductReview.objects.filter(is_published=True).order_by('-created_at'),
                to_attr='published_reviews',
            ),
        ),
        slug=slug,
    )
    product.views_count = models_f_add(product)

    video_url = (product.video_url or '').strip()
    video_direct = ''
    video_embed = ''
    if product.video_file:
        try:
            video_direct = product.video_file.url
        except ValueError:
            video_direct = ''
    if not video_direct and video_url:
        if is_direct_video(video_url):
            video_direct = video_url
        else:
            video_embed = youtube_embed_url(video_url)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related': related_products(product),
        'reviews': getattr(product, 'published_reviews', []),
        'video_embed_url': video_embed,
        'video_direct': video_direct,
        'primary_image': product.images.first(),
    })


def models_f_add(product: Product) -> int:
    Product.objects.filter(pk=product.pk).update(views_count=product.views_count + 1)
    return product.views_count + 1


@require_GET
def search_suggest(request):
    q = sanitize_search_query(request.GET.get('q'))
    products = []
    try:
        if len(q) >= SUGGEST_MIN_LEN:
            products = list(
                Product.objects.on_storefront()
                .filter(product_search_q(q))
                .select_related('brand')
                .prefetch_related('images')
                .order_by('sort_order', 'name', 'id')[:8]
            )
    except (DatabaseError, ValueError, TypeError):
        products = []
    return render(request, 'catalog/partials/search_suggest.html', {
        'products': products,
        'q': q,
    })
