from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
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


@login_required
def cabinet(request):
    orders = Order.objects.filter(user=request.user)[:20]
    wishlist = request.user.wishlist.select_related('product', 'product__brand')[:40]
    addresses = request.user.addresses.all()
    return render(request, 'accounts/cabinet.html', {
        'orders': orders,
        'wishlist': wishlist,
        'addresses': addresses,
    })
