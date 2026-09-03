from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from apps.catalog.browser_filters import (
    apply_category_params,
    apply_filters,
    build_browser_context,
)
from apps.catalog.models import Brand, Category, Product


def catalog_list(request, slug=None):
    qs = Product.objects.on_storefront().with_relations()
    category = None
    if slug:
        category = get_object_or_404(Category, slug=slug, is_active=True)
    qs = apply_category_params(qs, request.GET, path_category=category)
    qs = apply_filters(qs, request.GET)
    products = list(qs[:48])
    ctx = build_browser_context(request, products=products, category=category)
    if request.htmx:
        return render(request, 'catalog/partials/product_grid.html', ctx)
    return render(request, 'catalog/list.html', ctx)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    qs = Product.objects.on_storefront().with_relations().filter(brand=brand)
    qs = apply_category_params(qs, request.GET, path_category=None)
    qs = apply_filters(qs, request.GET)
    products = list(qs[:48])
    ctx = build_browser_context(request, products=products, brand=brand)
    if request.htmx:
        return render(request, 'catalog/partials/product_grid.html', ctx)
    return render(request, 'catalog/list.html', ctx)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.on_storefront().with_relations(),
        slug=slug,
    )
    product.views_count = models_f_add(product)
    variant_slug = request.GET.get('vitola')
    active_variant = None
    variants = list(product.variants.filter(is_active=True))
    if variant_slug:
        active_variant = next((v for v in variants if v.slug == variant_slug), None)
    if active_variant is None and variants:
        active_variant = variants[0]

    related = (
        Product.objects.on_storefront()
        .with_relations()
        .filter(brand=product.brand)
        .exclude(pk=product.pk)[:4]
    )
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'variants': variants,
        'active_variant': active_variant,
        'related': related,
    })


def models_f_add(product: Product) -> int:
    Product.objects.filter(pk=product.pk).update(views_count=product.views_count + 1)
    return product.views_count + 1


@require_GET
def search_suggest(request):
    q = (request.GET.get('q') or '').strip()
    products = []
    if len(q) >= 2:
        products = list(
            Product.objects.on_storefront()
            .filter(
                Q(name__icontains=q) | Q(brand__name__icontains=q)
            )
            .select_related('brand')
            .prefetch_related('images')[:8]
        )
    return render(request, 'catalog/partials/search_suggest.html', {
        'products': products,
        'q': q,
    })
