"""Build site-wide breadcrumb trails from the current request."""

from __future__ import annotations

from django.urls import reverse

from apps.catalog.models import Brand, Category, Product


def _crumb(title: str, url: str | None = None) -> dict:
    return {'title': title, 'url': url}


def _category_chain(category: Category) -> list[dict]:
    chain: list[Category] = []
    current: Category | None = category
    seen: set[int] = set()
    while current is not None and current.pk not in seen:
        seen.add(current.pk)
        chain.append(current)
        current = current.parent
    chain.reverse()
    return [
        _crumb(c.name, reverse('catalog:category', kwargs={'slug': c.slug}))
        for c in chain
    ]


def _static_label(namespace: str | None, url_name: str | None, kwargs: dict) -> str | None:
    key = f'{namespace}:{url_name}' if namespace else url_name
    labels = {
        'catalog:list': 'Каталог',
        'cart:detail': 'Кошик',
        'orders:checkout': 'Оформлення',
        'orders:thank_you': 'Дякуємо',
        'accounts:login': 'Вхід',
        'accounts:register': 'Реєстрація',
        'accounts:cabinet': 'Кабінет',
        'pages:about': 'Про нас',
        'pages:faq': 'FAQ',
        'pages:legal': 'Правова інформація',
        'leads:b2b': 'B2B',
        'leads:delivery': 'Доставка і оплата',
        'leads:contact': 'Контакти',
    }
    if key == 'pages:legal':
        slug = kwargs.get('slug') or 'privacy'
        legal_map = {
            'privacy': 'Політика конфіденційності',
            'terms': 'Умови користування',
            'age': 'Вікова політика',
            'cookies': 'Файли cookie',
        }
        return legal_map.get(slug, 'Правова інформація')
    return labels.get(key)


def build_breadcrumbs(request) -> list[dict]:
    match = getattr(request, 'resolver_match', None)
    if not match:
        return []

    namespace = match.namespace
    url_name = match.url_name
    kwargs = match.kwargs or {}

    if namespace == 'pages' and url_name == 'home':
        return []

    # HTMX partials / search suggest — no crumbs
    if namespace == 'catalog' and url_name == 'search':
        return []

    home = _crumb('Головна', reverse('pages:home'))
    crumbs: list[dict] = [home]

    if namespace == 'catalog' and url_name == 'list':
        crumbs.append(_crumb('Каталог'))
        return crumbs

    if namespace == 'catalog' and url_name == 'category':
        crumbs.append(_crumb('Каталог', reverse('catalog:list')))
        category = Category.objects.filter(
            slug=kwargs.get('slug'), is_active=True,
        ).select_related('parent').first()
        if category:
            chain = _category_chain(category)
            for item in chain[:-1]:
                crumbs.append(item)
            if chain:
                crumbs.append(_crumb(chain[-1]['title']))
        else:
            crumbs.append(_crumb('Каталог'))
        return crumbs

    if namespace == 'catalog' and url_name == 'brand':
        crumbs.append(_crumb('Каталог', reverse('catalog:list')))
        brand = Brand.objects.filter(slug=kwargs.get('slug'), is_active=True).first()
        crumbs.append(_crumb(brand.name if brand else 'Бренд'))
        return crumbs

    if namespace == 'catalog' and url_name == 'product':
        crumbs.append(_crumb('Каталог', reverse('catalog:list')))
        product = (
            Product.objects.on_storefront()
            .select_related('brand', 'category', 'category__parent')
            .filter(slug=kwargs.get('slug'))
            .first()
        )
        if product:
            for item in _category_chain(product.category):
                crumbs.append(item)
            if product.brand_id:
                crumbs.append(_crumb(
                    product.brand.name,
                    reverse('catalog:brand', kwargs={'slug': product.brand.slug}),
                ))
            crumbs.append(_crumb(product.name))
        else:
            crumbs.append(_crumb('Товар'))
        return crumbs

    label = _static_label(namespace, url_name, kwargs)
    if label:
        crumbs.append(_crumb(label))
        return crumbs

    return []
