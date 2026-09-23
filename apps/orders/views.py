from __future__ import annotations

import logging
import secrets
from decimal import Decimal, InvalidOperation

from django import forms
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.cart import services as cart_services
from apps.core.currency import convert_cart_totals
from apps.core.validation import EmailField, NameField, PhoneField
from apps.orders.access import can_view_order, grant_order_access
from apps.orders.checkout_session import checkout_expiry_context, touch_checkout_session
from apps.orders.models import Order, OrderItem, Payment
from apps.orders.services import notify_order_created
from apps.orders.services import liqpay as liqpay_svc
from apps.orders.services import nova_poshta as np_svc
from apps.orders.services import payments as pay_svc

logger = logging.getLogger(__name__)

CHECKOUT_TOKEN_KEY = 'rs_checkout_token'
LAST_ORDER_KEY = 'rs_last_order'
ORDER_DONE_FLASH_KEY = 'rs_order_done_flash'


def _no_store(response):
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    return response


def _issue_checkout_token(session) -> str:
    token = secrets.token_urlsafe(24)
    session[CHECKOUT_TOKEN_KEY] = token
    session.modified = True
    return token


def _consume_checkout_token(session, submitted: str | None) -> bool:
    expected = session.pop(CHECKOUT_TOKEN_KEY, None)
    session.modified = True
    if not expected or not submitted:
        return False
    return secrets.compare_digest(str(expected), str(submitted))


def _mark_order_done(session, order_number: str) -> None:
    session[LAST_ORDER_KEY] = order_number
    session[ORDER_DONE_FLASH_KEY] = True
    grant_order_access(session, order_number)
    session.modified = True


def _require_order_access(request, order):
    if can_view_order(request, order):
        return None
    return HttpResponseForbidden(_('Немає доступу до цього замовлення'))


def _empty_cart_after_order_response(request):
    last = request.session.get(LAST_ORDER_KEY)
    request.session.pop(ORDER_DONE_FLASH_KEY, None)
    messages.info(request, _('Замовлення вже створено'))
    if last and Order.objects.filter(order_number=last).exists():
        return redirect('orders:thank_you', order_number=last)
    return redirect('cart:detail')


class CheckoutForm(forms.Form):
    first_name = NameField(label=_lazy('Імʼя'), max_length=100)
    last_name = NameField(label=_lazy('Прізвище'), max_length=100)
    phone = PhoneField(label=_lazy('Телефон'))
    email = EmailField(label=_lazy('Email'))
    delivery_service = forms.ChoiceField(label=_lazy('Доставка'), choices=Order.DELIVERY_CHOICES)
    delivery_city = forms.CharField(label=_lazy('Місто'), max_length=150)
    delivery_address = forms.CharField(label=_lazy('Адреса / відділення'), max_length=255)
    np_city_ref = forms.CharField(required=False, max_length=64)
    np_warehouse_ref = forms.CharField(required=False, max_length=64)
    payment_method = forms.ChoiceField(label=_lazy('Оплата'), choices=Order.PAYMENT_CHOICES)
    comment = forms.CharField(
        label=_lazy('Коментар'), required=False, widget=forms.Textarea(attrs={'rows': 3}),
    )
    delivery_cost = forms.DecimalField(required=False, min_value=0, max_digits=12, decimal_places=2)
    age_confirm = forms.BooleanField(label=_lazy('Підтвердження віку'))

    def clean_age_confirm(self):
        if not self.cleaned_data.get('age_confirm'):
            raise forms.ValidationError(_('Потрібно підтвердити вік 21+'))
        return True

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('delivery_service') == Order.DELIVERY_NP:
            if not cleaned.get('np_city_ref') or not cleaned.get('np_warehouse_ref'):
                self.add_error(
                    'delivery_address',
                    _('Оберіть місто та відділення Нової Пошти зі списку'),
                )
            else:
                status = np_svc.warehouse_status(
                    cleaned.get('np_city_ref') or '',
                    cleaned.get('np_warehouse_ref') or '',
                )
                if status == 'missing':
                    self.add_error(
                        'delivery_address',
                        _('Обране відділення більше недоступне. Оберіть інше зі списку.'),
                    )
                elif status == 'unverified':
                    cleaned['np_unverified'] = True
        return cleaned


def _create_order_from_cart(request, data, totals, *, idempotency_key: str) -> Order:
    from apps.core.money import MIN_UNIT_PRICE, money, reconcile_order_totals

    delivery_cost = data.get('delivery_cost') or Decimal('0')
    try:
        delivery_cost = Decimal(delivery_cost)
    except (InvalidOperation, TypeError):
        delivery_cost = Decimal('0')
    priced = convert_cart_totals(totals, delivery_cost)
    if money(priced['total']) < MIN_UNIT_PRICE:
        raise ValueError('order total must be positive')
    status = Order.STATUS_PENDING
    if data['payment_method'] == Order.PAYMENT_ONLINE:
        status = Order.STATUS_AWAITING_PAYMENT
    comment = data.get('comment') or ''
    if data.get('np_unverified'):
        marker = '[RS:NP_UNVERIFIED] Відділення НП не перевірено (API недоступне).'
        comment = f'{marker}\n{comment}'.strip() if comment else marker
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data['email'],
        comment=comment,
        delivery_service=data['delivery_service'],
        delivery_city=data['delivery_city'],
        delivery_address=data['delivery_address'],
        np_city_ref=data.get('np_city_ref') or '',
        np_warehouse_ref=data.get('np_warehouse_ref') or '',
        payment_method=data['payment_method'],
        subtotal=money(priced['subtotal']),
        discount=money(priced.get('discount') or 0),
        delivery_cost=money(priced['delivery_cost']),
        total=money(priced['total']),
        currency=priced['currency'],
        fx_rate=priced['fx_rate'],
        market=getattr(settings, 'DEFAULT_MARKET', 'UA'),
        status=status,
        idempotency_key=idempotency_key,
    )
    for item in priced['items']:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            product_name=str(item['product']),
            product_sku=item['product'].sku or '',
            price=money(item['unit_price']),
            quantity=item['quantity'],
            line_total=money(item['line_total']),
        )
    reconcile_order_totals(order)
    return order


@require_http_methods(['GET', 'POST'])
def checkout(request):
    touch_checkout_session(request)
    totals = cart_services.cart_totals(request.session)
    if not totals['items']:
        if request.session.get(LAST_ORDER_KEY) or request.session.get(ORDER_DONE_FLASH_KEY):
            return _no_store(_empty_cart_after_order_response(request))
        messages.warning(request, _('Кошик порожній'))
        return _no_store(redirect('cart:detail'))

    issues = totals.get('issues') or []
    if issues and request.method == 'POST':
        for text in issues:
            messages.warning(request, text)
        messages.error(request, _('Оформлення заблоковано через наявність товарів'))
        return _no_store(redirect('orders:checkout'))

    initial = {'delivery_cost': Decimal('0')}
    if request.user.is_authenticated:
        initial.update({
            'email': request.user.email,
            'phone': request.user.phone,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    form = CheckoutForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        from django.db import IntegrityError

        from apps.orders.idempotency import checkout_idempotency_key, tokens_match

        submitted_token = request.POST.get('checkout_token') or ''
        idem_key = checkout_idempotency_key(submitted_token) if submitted_token else ''
        existing = Order.objects.filter(idempotency_key=idem_key).first() if idem_key else None
        if existing:
            _mark_order_done(request.session, existing.order_number)
            messages.info(request, _('Замовлення вже створено'))
            if existing.payment_method == Order.PAYMENT_ONLINE:
                return _no_store(redirect('orders:pay', order_number=existing.order_number))
            return _no_store(redirect(existing.get_absolute_url()))

        session_token = request.session.get(CHECKOUT_TOKEN_KEY)
        if not tokens_match(session_token, submitted_token):
            messages.info(request, _('Замовлення вже створено'))
            last = request.session.get(LAST_ORDER_KEY)
            if last and Order.objects.filter(order_number=last).exists():
                return _no_store(redirect('orders:thank_you', order_number=last))
            return _no_store(redirect('cart:detail'))
        request.session.pop(CHECKOUT_TOKEN_KEY, None)
        request.session.modified = True

        from apps.cart import stock as stock_svc
        created = False
        with transaction.atomic():
            consume_issues = stock_svc.consume_for_checkout(
                totals['items'],
                session=request.session,
                user=request.user if request.user.is_authenticated else None,
            )
            if consume_issues:
                for text in consume_issues:
                    messages.warning(request, text)
                messages.error(request, _('Оформлення заблоковано через наявність товарів'))
                return _no_store(redirect('orders:checkout'))
            try:
                order = _create_order_from_cart(
                    request, form.cleaned_data, totals, idempotency_key=idem_key,
                )
                created = True
            except IntegrityError:
                existing = Order.objects.filter(idempotency_key=idem_key).first()
                if existing:
                    order = existing
                else:
                    raise
            except ValueError:
                messages.error(request, _('Оформлення заблоковано: некоректна сума замовлення'))
                return _no_store(redirect('orders:checkout'))
            cart_services.clear(request.session)
            if request.user.is_authenticated:
                from apps.cart import db_services as db_cart
                db_cart.clear(request.user)
            _mark_order_done(request.session, order.order_number)
        if created:
            notify_order_created(order)
        else:
            messages.info(request, _('Замовлення вже створено'))
        if order.payment_method == Order.PAYMENT_ONLINE:
            return _no_store(redirect('orders:pay', order_number=order.order_number))
        return _no_store(redirect(order.get_absolute_url()))

    checkout_token = _issue_checkout_token(request.session)
    ctx = {
        'form': form,
        'cart': totals,
        'cart_issues': issues,
        'can_checkout': totals.get('can_checkout', not issues),
        'checkout_token': checkout_token,
        'delivery_cost': form['delivery_cost'].value() or 0,
        'grand_total': totals['total'],
        'demo_payments': pay_svc.demo_payments_enabled(),
    }
    ctx.update(checkout_expiry_context(request))
    return _no_store(render(request, 'orders/checkout.html', ctx))


def thank_you(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    denied = _require_order_access(request, order)
    if denied:
        return denied
    return _no_store(render(request, 'orders/thank_you.html', {'order': order}))


def _payment_gate(order: Order) -> str:
    """paid | waiting | retry | new — controls /pay/ behaviour."""
    payment = Payment.objects.filter(liqpay_order_id=order.order_number).first()
    if order.status == Order.STATUS_PAID:
        return 'paid'
    if payment and payment.status == Payment.STATUS_SUCCESS:
        return 'paid'
    if payment and payment.status == Payment.STATUS_PENDING:
        return 'waiting'
    if payment and payment.status in (Payment.STATUS_FAILURE, Payment.STATUS_REVERSED):
        return 'retry'
    return 'new'


@require_GET
def pay(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    denied = _require_order_access(request, order)
    if denied:
        return denied
    if order.payment_method != Order.PAYMENT_ONLINE:
        return redirect(order.get_absolute_url())

    touch_checkout_session(request)

    gate = _payment_gate(order)
    if gate == 'paid':
        messages.info(request, _('Замовлення вже оплачено'))
        return _no_store(redirect(order.get_absolute_url()))

    from apps.core.money import reconcile_order_totals
    try:
        reconcile_order_totals(order)
    except ValueError:
        messages.error(request, _('Суму замовлення неможливо підтвердити. Звʼяжіться з підтримкою.'))
        return redirect(order.get_absolute_url())

    demo = pay_svc.demo_payments_enabled()

    # Callback delayed / invoice already issued — do not open a second LiqPay charge.
    if gate == 'waiting' and not demo:
        return _no_store(render(request, 'orders/pay.html', {
            'order': order,
            'demo': False,
            'waiting': True,
        }))

    if demo:
        pay_svc.ensure_pending_payment(order, provider=Payment.PROVIDER_DEMO)
        return _no_store(render(request, 'orders/pay.html', {
            'order': order,
            'demo': True,
            'waiting': False,
        }))

    try:
        payload = liqpay_svc.create_checkout_payload(
            order,
            result_url=request.build_absolute_uri(
                reverse('orders_liqpay_result') + f'?order={order.order_number}'
            ),
            server_url=request.build_absolute_uri(reverse('orders_liqpay_callback')),
        )
    except ValueError:
        messages.error(request, _('Онлайн-оплата тимчасово недоступна'))
        return redirect(order.get_absolute_url())
    pay_svc.ensure_pending_payment(order, provider=Payment.PROVIDER_LIQPAY)
    return _no_store(render(request, 'orders/pay.html', {
        'order': order,
        'demo': False,
        'waiting': False,
        'data': payload['data'],
        'signature': payload['signature'],
        'checkout_url': payload['checkout_url'],
    }))


@require_POST
def demo_pay(request, order_number):
    if not pay_svc.demo_payments_enabled():
        return HttpResponseForbidden('demo payments disabled')
    order = get_object_or_404(Order, order_number=order_number)
    denied = _require_order_access(request, order)
    if denied:
        return denied
    if order.payment_method != Order.PAYMENT_ONLINE:
        return redirect(order.get_absolute_url())
    if _payment_gate(order) == 'paid':
        messages.info(request, _('Замовлення вже оплачено'))
        return redirect(order.get_absolute_url())
    outcome = (request.POST.get('outcome') or 'success').lower()
    status = 'success' if outcome == 'success' else 'failure'
    paid_now = pay_svc.settle_payment(
        order,
        status=status,
        payload={'demo': True, 'status': status, 'order_id': order.order_number},
        provider=Payment.PROVIDER_DEMO,
        transaction_id=f'demo-{order.order_number}',
    )
    if status == 'success':
        if paid_now:
            messages.success(request, _('Демо-оплату підтверджено.'))
        else:
            messages.info(request, _('Замовлення вже оплачено'))
    else:
        messages.error(request, _('Демо-оплату відхилено. Можна спробувати ще раз.'))
    return redirect(order.get_absolute_url())


@csrf_exempt
@require_POST
def liqpay_callback(request):
    data = request.POST.get('data', '')
    signature = request.POST.get('signature', '')
    try:
        payload = liqpay_svc.verify_callback(data, signature)
    except ValueError:
        return HttpResponseBadRequest('invalid signature')
    order_id = payload.get('order_id') or ''
    status = (payload.get('status') or '').lower()
    try:
        order = Order.objects.get(order_number=order_id)
    except Order.DoesNotExist:
        logger.warning('LiqPay callback for unknown order %s', order_id)
        return HttpResponse('ok')
    pay_svc.settle_payment(
        order,
        status=status,
        payload=payload,
        provider=Payment.PROVIDER_LIQPAY,
        transaction_id=str(payload.get('transaction_id') or payload.get('payment_id') or ''),
    )
    return HttpResponse('ok')

@require_GET
def liqpay_result(request):
    order_number = request.GET.get('order') or ''
    order = get_object_or_404(Order, order_number=order_number)
    return redirect(order.get_absolute_url())


@require_GET
def np_cities(request):
    q = request.GET.get('q') or request.GET.get('delivery_city') or ''
    cities = []
    try:
        cities = np_svc.search_cities(q)
    except np_svc.NovaPoshtaError:
        logger.exception('NP cities search failed')
    return render(request, 'orders/partials/np_cities.html', {
        'cities': cities,
        'q': q,
    })


@require_GET
def np_warehouses(request):
    city_ref = (
        request.GET.get('city_ref')
        or request.GET.get('np_city_ref')
        or ''
    )
    q = request.GET.get('q') or request.GET.get('delivery_address') or ''
    warehouses = []
    try:
        warehouses = np_svc.get_warehouses(city_ref, q)
    except np_svc.NovaPoshtaError:
        logger.exception('NP warehouses search failed')
    return render(request, 'orders/partials/np_warehouses.html', {
        'warehouses': warehouses,
        'city_ref': city_ref,
        'q': q,
    })


@require_http_methods(['GET', 'POST'])
def np_cost(request):
    totals = cart_services.cart_totals(request.session)
    data = request.POST if request.method == 'POST' else request.GET
    city_ref = data.get('np_city_ref') or ''
    delivery_service = data.get('delivery_service') or ''
    cost = Decimal('0')
    if delivery_service == Order.DELIVERY_NP and city_ref:
        try:
            cost = np_svc.calculate_delivery_cost(
                city_ref,
                weight_kg=1,
                cost=totals.get('subtotal') or 100,
            )
        except np_svc.NovaPoshtaError:
            logger.exception('NP cost calc failed')
            cost = Decimal('0')
    grand = (totals.get('subtotal') or Decimal('0')) + cost
    response = render(request, 'orders/partials/checkout_costs.html', {
        'cart': totals,
        'delivery_cost': cost,
        'grand_total': grand,
    })
    response['HX-Trigger'] = f'{{"rsDeliveryCost": {{"cost": "{cost}"}}}}'
    # also update hidden field via OOB would be nicer; use header + small script in base if needed
    return HttpResponse(
        response.content.decode('utf-8')
        + f'<input type="hidden" name="delivery_cost" id="id_delivery_cost" value="{cost}" '
        f'hx-swap-oob="true">'
    )
