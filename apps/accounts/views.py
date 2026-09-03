from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.accounts.forms import EmailAuthenticationForm, RegisterForm
from apps.orders.models import Order


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:cabinet')
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get('next') or 'accounts:cabinet')
    return render(request, 'accounts/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:cabinet')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
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
        or (request.user.email.split('@')[0] if request.user.email else 'гість')
    )
    initial = (display_name[:1] or '?').upper()
    return render(request, 'accounts/cabinet.html', {
        'orders': orders,
        'recent_order': recent_order,
        'chart_series': chart_series,
        'display_name': display_name,
        'avatar_initial': initial,
    })
