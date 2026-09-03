from decimal import Decimal

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views.decorators.http import require_http_methods

from apps.cart import services as cart_services
from apps.core.validation import EmailField, NameField, PhoneField
from apps.orders.models import Order, OrderItem


class CheckoutForm(forms.Form):
    first_name = NameField(label=_lazy('Імʼя'), max_length=100)
    last_name = NameField(label=_lazy('Прізвище'), max_length=100)
    phone = PhoneField(label=_lazy('Телефон'))
    email = EmailField(label=_lazy('Email'))
    delivery_service = forms.ChoiceField(label=_lazy('Доставка'), choices=Order.DELIVERY_CHOICES)
    delivery_city = forms.CharField(label=_lazy('Місто'), max_length=150)
    delivery_address = forms.CharField(label=_lazy('Адреса / відділення'), max_length=255)
    payment_method = forms.ChoiceField(label=_lazy('Оплата'), choices=Order.PAYMENT_CHOICES)
    comment = forms.CharField(
        label=_lazy('Коментар'), required=False, widget=forms.Textarea(attrs={'rows': 3}),
    )


@require_http_methods(['GET', 'POST'])
def checkout(request):
    totals = cart_services.cart_totals(request.session)
    if not totals['items']:
        messages.warning(request, _('Кошик порожній'))
        return redirect('cart:detail')

    initial = {}
    if request.user.is_authenticated:
        initial = {
            'email': request.user.email,
            'phone': request.user.phone,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }

    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            email=data['email'],
            comment=data.get('comment') or '',
            delivery_service=data['delivery_service'],
            delivery_city=data['delivery_city'],
            delivery_address=data['delivery_address'],
            payment_method=data['payment_method'],
            subtotal=totals['subtotal'],
            discount=Decimal('0'),
            delivery_cost=Decimal('0'),
            total=totals['total'],
            currency=getattr(settings, 'CURRENCY_CODE', 'UAH'),
            market=getattr(settings, 'DEFAULT_MARKET', 'UA'),
            status=Order.STATUS_PENDING,
        )
        for item in totals['items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                variant=item['variant'],
                product_name=str(item['product']),
                variant_name=item['variant'].name if item['variant'] else '',
                product_sku=(item['variant'].sku if item['variant'] else item['product'].sku) or '',
                price=item['unit_price'],
                quantity=item['quantity'],
                line_total=item['line_total'],
            )
        cart_services.clear(request.session)
        try:
            send_mail(
                f'Нове замовлення {order.order_number}',
                f'Замовлення {order.order_number} на суму {order.total} {order.currency}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.NOTIFY_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        return redirect(order.get_absolute_url())

    return render(request, 'orders/checkout.html', {'form': form, 'cart': totals})


def thank_you(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/thank_you.html', {'order': order})
