from apps.cart.services import cart_totals


def cart_context(request):
    totals = cart_totals(request.session)
    return {
        'cart_count': totals['count'],
        'cart_subtotal': totals['subtotal'],
    }
