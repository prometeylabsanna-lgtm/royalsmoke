from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.cart import db_services as db_cart
from apps.cart import services as cart_services
from apps.cart.qty import parse_product_id, parse_quantity


def _post_ids(request):
    product_id = parse_product_id(request.POST.get('product_id'))
    qty = parse_quantity(request.POST.get('quantity'), default=1)
    return product_id, qty


def _persist_auth(request) -> None:
    if request.user.is_authenticated:
        db_cart.replace_from_session(request.session, request.user)


def _flash_order_done(request) -> None:
    if request.session.pop('rs_order_done_flash', None):
        from django.contrib import messages
        from django.utils.translation import gettext as _
        messages.info(request, _('Замовлення вже створено'))


def cart_detail(request):
    _flash_order_done(request)
    totals = cart_services.cart_totals(request.session)
    return render(request, 'cart/cart.html', {'cart': totals})


@require_GET
def cart_badge(request):
    totals = cart_services.cart_totals(request.session)
    return render(request, 'cart/partials/badge.html', {
        'cart_count': totals['count'],
    })


def _htmx_cart_response(request, totals):
    target = (request.headers.get('HX-Target') or '').lstrip('#')
    if target == 'cart-body':
        return render(request, 'cart/partials/cart_body_htmx.html', {
            'cart': totals,
            'cart_count': totals['count'],
        })
    return render(request, 'cart/partials/badge.html', {
        'cart_count': totals['count'],
    })


@require_POST
def cart_add(request):
    product_id, qty = _post_ids(request)
    if product_id and qty >= 1:
        try:
            cart_services.add_item(request.session, product_id, qty)
            _persist_auth(request)
        except Http404:
            pass
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return _htmx_cart_response(request, totals)
    return redirect('cart:detail')


@require_POST
def cart_update(request):
    product_id, qty = _post_ids(request)
    if product_id:
        try:
            cart_services.set_quantity(request.session, product_id, qty)
            _persist_auth(request)
        except Http404:
            pass
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return _htmx_cart_response(request, totals)
    return redirect('cart:detail')


@require_POST
def cart_remove(request):
    product_id, _qty = _post_ids(request)
    if product_id:
        cart_services.remove_item(request.session, product_id)
        _persist_auth(request)
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return _htmx_cart_response(request, totals)
    return redirect('cart:detail')
