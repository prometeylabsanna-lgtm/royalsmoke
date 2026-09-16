from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods, require_POST

from apps.accounts import wishlist as wishlist_services
from apps.accounts.forms import EmailAuthenticationForm, RegisterForm
from apps.catalog.models import Product
from apps.orders.models import Order


def _safe_next(request, fallback: str = 'accounts:cabinet'):
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return fallback


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:cabinet')
    next_url = request.POST.get('next') or request.GET.get('next') or ''
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        wishlist_services.merge_session_to_user(request)
        return redirect(_safe_next(request))
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:cabinet')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        wishlist_services.merge_session_to_user(request)
        return redirect('accounts:cabinet')
    return render(request, 'accounts/register.html', {'form': form})


def _cabinet_chart(user, weeks: int = 8) -> list[dict]:
    """Weekly order totals for the last N weeks → bar heights 8–100%."""
    today = timezone.localdate()
    this_monday = today - timedelta(days=today.weekday())
    range_start = this_monday - timedelta(weeks=weeks - 1)

    orders = Order.objects.filter(
        user=user,
        created_at__date__gte=range_start,
    ).values_list('created_at', 'total')

    buckets = [Decimal('0')] * weeks
    for created_at, total in orders:
        local_d = timezone.localtime(created_at).date()
        monday = local_d - timedelta(days=local_d.weekday())
        idx = (monday - range_start).days // 7
        if 0 <= idx < weeks:
            buckets[idx] += total or Decimal('0')

    max_total = max(buckets) if buckets else Decimal('0')
    series: list[dict] = []
    for i, total in enumerate(buckets):
        height = 8
        if max_total > 0:
            height = min(100, int((total / max_total) * 92) + 8)
        series.append({
            'start': range_start + timedelta(weeks=i),
            'total': total,
            'height': height,
        })
    return series


@login_required
def cabinet(request):
    orders = list(Order.objects.filter(user=request.user)[:20])
    recent_order = orders[0] if orders else None
    chart_series = _cabinet_chart(request.user)
    display_name = (
        request.user.get_full_name()
        or (request.user.first_name or '')
        or (request.user.email.split('@')[0] if request.user.email else _('гість'))
    )
    initial = (display_name[:1] or '?').upper()
    wishlist_items = wishlist_services.items(request)
    return render(request, 'accounts/cabinet.html', {
        'orders': orders,
        'recent_order': recent_order,
        'chart_series': chart_series,
        'display_name': display_name,
        'avatar_initial': initial,
        'wishlist_items': wishlist_items,
    })


def wishlist_detail(request):
    products = wishlist_services.items(request)
    return render(request, 'accounts/wishlist.html', {
        'products': products,
        'wishlist_count': len(products),
    })


def _badge_oob(request) -> str:
    return render_to_string(
        'accounts/partials/wishlist_badge.html',
        {'wishlist_count': wishlist_services.count(request), 'oob': True},
        request=request,
    )


@require_POST
def wishlist_toggle(request):
    try:
        product_id = int(request.POST.get('product_id', 0))
    except (TypeError, ValueError):
        product_id = 0
    if product_id:
        wishlist_services.toggle(request, product_id)

    if not request.htmx:
        return redirect('accounts:wishlist')

    target = request.htmx.target or ''
    products = wishlist_services.items(request)
    ids = wishlist_services.product_ids(request)

    if target == 'wishlist-body':
        body = render_to_string(
            'accounts/partials/wishlist_body.html',
            {'products': products, 'wishlist_count': len(products)},
            request=request,
        )
        return HttpResponse(body + _badge_oob(request))

    if target == 'cabinet-wishlist':
        body = render_to_string(
            'accounts/partials/cabinet_wishlist.html',
            {'wishlist_items': products},
            request=request,
        )
        return HttpResponse(body + _badge_oob(request))

    product = Product.objects.filter(pk=product_id).first()
    if product:
        show_label = request.POST.get('wish_context') == 'pd'
        btn = render_to_string(
            'accounts/partials/wish_btn.html',
            {
                'product': product,
                'wishlist_ids': ids,
                'show_label': show_label,
            },
            request=request,
        )
        return HttpResponse(btn + _badge_oob(request))

    return HttpResponse(_badge_oob(request))
