from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.cart import services as cart_services


def _post_ids(request):
    try:
        product_id = int(request.POST.get('product_id') or 0)
    except (TypeError, ValueError):
        product_id = 0
    raw_variant = request.POST.get('variant_id') or None
    variant_id = None
    if raw_variant:
        try:
            variant_id = int(raw_variant)
        except (TypeError, ValueError):
            variant_id = None
    try:
        qty = int(request.POST.get('quantity') or 1)
    except (TypeError, ValueError):
        qty = 1
    return product_id, variant_id, qty


def cart_detail(request):
    totals = cart_services.cart_totals(request.session)
    return render(request, 'cart/cart.html', {'cart': totals})


@require_POST
def cart_add(request):
    product_id, variant_id, qty = _post_ids(request)
    if product_id:
        try:
            cart_services.add_item(request.session, product_id, qty, variant_id)
        except Http404:
            pass
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/badge.html', {'cart_count': totals['count']})
    return redirect('cart:detail')


@require_POST
def cart_update(request):
    product_id, variant_id, qty = _post_ids(request)
    if product_id:
        try:
            cart_services.set_quantity(request.session, product_id, qty, variant_id)
        except Http404:
            pass
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/cart_body.html', {'cart': totals})
    return redirect('cart:detail')


@require_POST
def cart_remove(request):
    product_id, variant_id, _qty = _post_ids(request)
    if product_id:
        cart_services.remove_item(request.session, product_id, variant_id)
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/cart_body.html', {'cart': totals})
    return redirect('cart:detail')
