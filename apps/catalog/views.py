from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from apps.catalog.models import Brand, Category, Product, ProductVariant


def _apply_filters(qs, params):
    strength = params.getlist('strength') or ([params.get('strength')] if params.get('strength') else [])
    country = params.getlist('country')
    brand = params.getlist('brand')
    tag = (params.get('tag') or '').strip()
    q = (params.get('q') or '').strip()
    sort = params.get('sort') or 'default'

    strength = [s for s in strength if s]
    if strength:
        qs = qs.filter(strength__in=strength)
    if country:
        qs = qs.filter(country__in=country)
    if brand:
        qs = qs.filter(brand__slug__in=brand)
    if tag:
        qs = qs.filter(tags__slug=tag).distinct()
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(brand__name__icontains=q)
            | Q(description__icontains=q)
            | Q(short_story__icontains=q)
        )

    if sort in ('price_asc', 'price'):
        qs = qs.order_by('base_price', 'name')
    elif sort in ('price_desc', '-price'):
        qs = qs.order_by('-base_price', 'name')
    elif sort == 'name':
        qs = qs.order_by('name')
    elif sort == 'new':
        qs = qs.order_by('-created_at')
    else:
        qs = qs.order_by('sort_order', 'name')
    return qs


def catalog_list(request, slug=None):
    qs = Product.objects.on_storefront().with_relations()
    category = None
    if slug:
        category = get_object_or_404(Category, slug=slug, is_active=True)
        qs = qs.filter(Q(category=category) | Q(category__parent=category))
    qs = _apply_filters(qs, request.GET)
    products = list(qs[:48])

    facets = {
        'strengths': Product.Strength.choices,
        'countries': (
            Product.objects.on_storefront()
            .exclude(country='')
            .order_by('country')
            .values_list('country', flat=True)
            .distinct()
        ),
        'brands': Brand.objects.filter(is_active=True).order_by('name'),
        'categories': Category.objects.filter(is_active=True, parent__isnull=True),
    }
    ctx = {
        'products': products,
        'category': category,
        'facets': facets,
        'current_filters': request.GET,
    }
    if request.htmx:
        return render(request, 'catalog/partials/product_grid.html', ctx)
    return render(request, 'catalog/list.html', ctx)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.on_storefront().with_relations().filter(brand=brand)[:48]
    return render(request, 'catalog/list.html', {
        'products': products,
        'brand': brand,
        'facets': {
            'strengths': Product.Strength.choices,
            'countries': [],
            'brands': Brand.objects.filter(is_active=True),
            'categories': Category.objects.filter(is_active=True, parent__isnull=True),
        },
        'current_filters': request.GET,
    })


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
            .filter(Q(name__icontains=q) | Q(brand__name__icontains=q))
            .select_related('brand')[:8]
        )
    return render(request, 'catalog/partials/search_results.html', {'products': products, 'q': q})
