from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from apps.cart import services as cart_services


def cart_detail(request):
    totals = cart_services.cart_totals(request.session)
    return render(request, 'cart/cart.html', {'cart': totals})


@require_POST
def cart_add(request):
    product_id = int(request.POST.get('product_id', 0))
    variant_id = request.POST.get('variant_id') or None
    qty = int(request.POST.get('quantity', 1) or 1)
    if variant_id:
        variant_id = int(variant_id)
    cart_services.add_item(request.session, product_id, qty, variant_id)
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/badge.html', {'cart_count': totals['count']})
    return redirect('cart:detail')


@require_POST
def cart_update(request):
    product_id = int(request.POST.get('product_id', 0))
    variant_id = request.POST.get('variant_id') or None
    qty = int(request.POST.get('quantity', 1) or 0)
    if variant_id:
        variant_id = int(variant_id)
    cart_services.set_quantity(request.session, product_id, qty, variant_id)
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/cart_body.html', {'cart': totals})
    return redirect('cart:detail')


@require_POST
def cart_remove(request):
    product_id = int(request.POST.get('product_id', 0))
    variant_id = request.POST.get('variant_id') or None
    if variant_id:
        variant_id = int(variant_id)
    cart_services.remove_item(request.session, product_id, variant_id)
    totals = cart_services.cart_totals(request.session)
    if request.htmx:
        return render(request, 'cart/partials/cart_body.html', {'cart': totals})
    return redirect('cart:detail')
