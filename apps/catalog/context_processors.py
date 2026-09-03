from apps.catalog import compare as compare_services


def compare_context(request):
    ids = compare_services.product_ids(request)
    return {
        'compare_ids': ids,
        'compare_count': len(ids),
    }
