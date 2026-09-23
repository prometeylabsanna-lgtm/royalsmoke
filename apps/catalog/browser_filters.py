"""Catalog browser filter helpers: multi-select, price range, sort."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from django.db.models import Count, Max, Min, Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Brand, Category, Product
from apps.catalog.search import product_search_q, sanitize_search_query
from apps.core.currency import convert_from_uah_int, convert_to_uah

SORT_OPTIONS = (
    ('top', _('Топ')),
    ('new', _('Новинки')),
    ('price_asc', _('Ціна ↑')),
    ('price_desc', _('Ціна ↓')),
)


def _as_decimal(raw, default=None):
    if raw is None or raw == '':
        return default
    try:
        return Decimal(str(raw))
    except (InvalidOperation, ValueError, TypeError):
        return default


def _clean_list(params, key):
    return [v for v in params.getlist(key) if v]


def price_bounds():
    agg = Product.objects.on_storefront().aggregate(
        mn=Min('base_price'),
        mx=Max('base_price'),
    )
    mn = agg['mn'] if agg['mn'] is not None else Decimal('0')
    mx = agg['mx'] if agg['mx'] is not None else Decimal('5000')
    if mx <= mn:
        mx = mn + Decimal('1')
    return int(mn), int(mx)


def apply_filters(qs, params):
    strength = _clean_list(params, 'strength')
    if not strength:
        single = (params.get('strength') or '').strip()
        if single:
            strength = [single]

    country = _clean_list(params, 'country')
    brand = _clean_list(params, 'brand')
    tag = (params.get('tag') or '').strip()
    q = sanitize_search_query(params.get('q'))
    sort = params.get('sort') or 'default'

    if strength:
        qs = qs.filter(strength__in=strength)
    if country:
        qs = qs.filter(country__in=country)
    if brand:
        qs = qs.filter(brand__slug__in=brand)
    if tag:
        qs = qs.filter(tags__slug=tag).distinct()
    if q:
        qs = qs.filter(product_search_q(q)).distinct()

    bound_min_uah, bound_max_uah = price_bounds()
    price_min = _as_decimal(params.get('price_min'))
    price_max = _as_decimal(params.get('price_max'))
    legacy = (params.get('price') or '').strip()

    if price_min is None and price_max is None and legacy:
        if legacy == 'lt1000':
            price_max = Decimal('999.99')
            qs = qs.filter(base_price__lte=price_max)
        elif legacy == '1000-2000':
            qs = qs.filter(base_price__gte=Decimal('1000'), base_price__lte=Decimal('2000'))
        elif legacy == 'gte2000':
            qs = qs.filter(base_price__gte=Decimal('2000'))
    else:
        if price_min is not None:
            price_min_uah = convert_to_uah(price_min)
            if price_min_uah > bound_min_uah:
                qs = qs.filter(base_price__gte=price_min_uah)
        if price_max is not None:
            price_max_uah = convert_to_uah(price_max)
            if price_max_uah < bound_max_uah:
                qs = qs.filter(base_price__lte=price_max_uah)

    # Always end with id for stable pagination (no duplicates/jumps across pages).
    if sort in ('price_asc', 'price'):
        qs = qs.order_by('base_price', 'name', 'id')
    elif sort in ('price_desc', '-price'):
        qs = qs.order_by('-base_price', 'name', 'id')
    elif sort == 'name':
        qs = qs.order_by('name', 'id')
    elif sort == 'new':
        qs = qs.order_by('-created_at', 'id')
    elif sort == 'top':
        qs = qs.order_by('-is_featured', 'sort_order', 'name', 'id')
    else:
        qs = qs.order_by('sort_order', 'name', 'id')
    return qs


def apply_category_params(qs, params, *, path_category=None):
    if path_category is not None:
        return qs.filter(
            Q(category=path_category) | Q(category__parent=path_category)
        )

    slugs = _clean_list(params, 'category')
    if not slugs:
        return qs
    return qs.filter(
        Q(category__slug__in=slugs) | Q(category__parent__slug__in=slugs)
    ).distinct()


def category_queryset():
    return (
        Category.objects.filter(is_active=True, parent__isnull=True)
        .exclude(slug='cigarettes')
        .exclude(name='Сигарети')
        .annotate(
            product_count=Count(
                'products',
                filter=Q(products__is_active=True, products__brand__is_active=True),
                distinct=True,
            )
        )
        .order_by('sort_order', 'name')
    )


def build_browser_context(request, *, products, category=None, brand=None, page_obj=None):
    params = request.GET
    list_path = reverse('catalog:list')
    if category:
        base_path = reverse('catalog:category', kwargs={'slug': category.slug})
    elif brand:
        base_path = reverse('catalog:brand', kwargs={'slug': brand.slug})
    else:
        base_path = list_path

    categories = list(category_queryset())
    selected_strength = set(_clean_list(params, 'strength'))
    if not selected_strength:
        single = (params.get('strength') or '').strip()
        if single:
            selected_strength = {single}

    selected_country = set(_clean_list(params, 'country'))
    selected_categories = set(_clean_list(params, 'category'))
    if category:
        selected_categories = {category.slug}
    all_categories_active = not selected_categories and not category

    bound_min_uah, bound_max_uah = price_bounds()
    bound_min = convert_from_uah_int(bound_min_uah)
    bound_max = convert_from_uah_int(bound_max_uah)
    if bound_max <= bound_min:
        bound_max = bound_min + 1
    price_min = _as_decimal(params.get('price_min'), Decimal(bound_min))
    price_max = _as_decimal(params.get('price_max'), Decimal(bound_max))
    price_min = max(Decimal(bound_min), min(price_min, Decimal(bound_max)))
    price_max = max(price_min, min(price_max, Decimal(bound_max)))

    current_tag = (params.get('tag') or '').strip()
    current_sort = (params.get('sort') or '').strip()
    current_q = sanitize_search_query(params.get('q'))

    nav_categories = []
    for cat in categories:
        nav_categories.append({
            'name': cat.name,
            'slug': cat.slug,
            'count': cat.product_count,
            'is_active': cat.slug in selected_categories,
        })

    strength_chips = [
        {
            'label': label,
            'value': value,
            'is_active': value in selected_strength,
        }
        for value, label in Product.Strength.choices
    ]
    # 3-step slider: Легка / (без підпису) / Повна
    strength_slider_map = [
        Product.Strength.MILD,
        Product.Strength.MEDIUM,
        Product.Strength.FULL,
    ]
    strength_slider_value = 0
    if len(selected_strength) == 1:
        only = next(iter(selected_strength))
        if only == Product.Strength.MEDIUM_FULL:
            only = Product.Strength.MEDIUM
        if only in strength_slider_map:
            strength_slider_value = strength_slider_map.index(only)

    countries = (
        Product.objects.on_storefront()
        .exclude(country='')
        .order_by('country')
        .values_list('country', flat=True)
        .distinct()
    )
    country_chips = [
        {
            'label': name,
            'value': name,
            'is_active': name in selected_country,
        }
        for name in countries
    ]

    sort_chips = [
        {
            'label': label,
            'value': value,
            'is_active': (
                current_sort == value
                or (value == 'price_asc' and current_sort in ('price', 'price_asc'))
                or (value == 'price_desc' and current_sort in ('-price', 'price_desc'))
            ),
        }
        for value, label in SORT_OPTIONS
    ]

    if brand:
        crumb = brand.name
    elif category:
        crumb = category.name
    elif len(selected_categories) == 1:
        slug = next(iter(selected_categories))
        match = next((c for c in categories if c.slug == slug), None)
        crumb = match.name if match else 'Усі'
    else:
        crumb = 'Усі'

    has_filters = any([
        selected_strength,
        selected_country,
        selected_categories and not category,
        int(price_min) > bound_min,
        int(price_max) < bound_max,
        current_tag,
        current_sort,
        current_q,
    ])

    page_links = []
    if page_obj is not None and getattr(page_obj, 'paginator', None):
        total_pages = page_obj.paginator.num_pages
        if total_pages > 1 or getattr(page_obj, 'out_of_range', False):
            qdict = params.copy()
            for num in range(1, total_pages + 1):
                qdict['page'] = str(num)
                page_links.append({
                    'number': num,
                    'url': f'{base_path}?{qdict.urlencode()}' if qdict else base_path,
                    'is_current': num == page_obj.number and not getattr(page_obj, 'out_of_range', False),
                })

    return {
        'products': products,
        'page_obj': page_obj,
        'page_links': page_links,
        'current_q': current_q,
        'category': category,
        'brand': brand,
        'nav_categories': nav_categories,
        'all_categories_active': all_categories_active,
        'strength_chips': strength_chips,
        'strength_slider_map': strength_slider_map,
        'strength_slider_value': strength_slider_value,
        'country_chips': country_chips,
        'sort_chips': sort_chips,
        'catalog_crumb': crumb,
        'reset_url': base_path if brand or category else list_path,
        'has_filters': has_filters,
        'filter_base_path': base_path,
        'filter_list_path': list_path,
        'price_bound_min': bound_min,
        'price_bound_max': bound_max,
        'price_min': int(price_min),
        'price_max': int(price_max),
        'current_sort': current_sort,
        'selected_strength': list(selected_strength),
        'selected_country': list(selected_country),
        'selected_categories': list(selected_categories),
        'facets': {
            'strengths': Product.Strength.choices,
            'countries': countries,
            'brands': Brand.objects.filter(is_active=True).order_by('name'),
            'categories': categories,
        },
        'current_filters': params,
    }
