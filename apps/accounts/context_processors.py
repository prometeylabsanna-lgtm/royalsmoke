from apps.accounts import wishlist as wishlist_services


def wishlist_context(request):
    ids = wishlist_services.product_ids(request)
    return {
        'wishlist_ids': ids,
        'wishlist_count': len(ids),
    }
