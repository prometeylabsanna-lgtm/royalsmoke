from __future__ import annotations

import logging
from datetime import datetime, time, timedelta

from django import forms
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.booking.models import Booking, BookingService, BookingSlot
from apps.core.services.notifications import notify_admins, notify_user, render_email
from apps.core.validation import EmailField, NameField, PhoneField

logger = logging.getLogger(__name__)


class BookingForm(forms.Form):
    service = forms.ModelChoiceField(
        label=_lazy('Послуга'),
        queryset=BookingService.objects.filter(is_active=True),
    )
    slot = forms.ModelChoiceField(
        label=_lazy('Слот'),
        queryset=BookingSlot.objects.none(),
    )
    name = NameField(label=_lazy('Імʼя'))
    phone = PhoneField(label=_lazy('Телефон'))
    email = EmailField(label=_lazy('Email'), optional=True)
    comment = forms.CharField(label=_lazy('Побажання'), required=False, max_length=500)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        service_id = None
        if self.data.get('service'):
            service_id = self.data.get('service')
        elif self.initial.get('service'):
            service_id = getattr(self.initial['service'], 'pk', self.initial['service'])
        qs = BookingSlot.objects.filter(
            is_active=True,
            starts_at__gte=timezone.now(),
        ).select_related('service')
        if service_id:
            qs = qs.filter(service_id=service_id)
        self.fields['slot'].queryset = qs.order_by('starts_at')

    def clean_slot(self):
        slot = self.cleaned_data['slot']
        if slot.starts_at < timezone.now():
            raise forms.ValidationError(_('Цей слот уже минув'))
        if slot.seats_left <= 0:
            raise forms.ValidationError(_('Немає вільних місць'))
        return slot


def _notify_booking(booking: Booking) -> None:
    ctx = {'booking': booking}
    text, html = render_email('booking_created', ctx)
    notify_admins(
        f'Нове бронювання #{booking.pk}',
        text,
        html=html,
        telegram_text=(
            f'📅 Бронювання #{booking.pk}\n'
            f'{booking.name} · {booking.phone}\n'
            f'{booking.slot}'
        ),
    )
    if booking.email:
        cust_text, cust_html = render_email('booking_created_customer', ctx)
        notify_user(
            booking.email,
            _('Бронювання прийнято'),
            cust_text,
            html=cust_html,
            user=booking.user,
        )


def _redirect_next(request, fallback: str = 'booking:page'):
    next_url = request.POST.get('next') or ''
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(fallback)


def _available_slots(service_id: int | None = None, day: datetime | None = None):
    qs = (
        BookingSlot.objects.filter(is_active=True, starts_at__gte=timezone.now())
        .select_related('service')
        .annotate(
            active_bookings=Count(
                'bookings',
                filter=~Q(bookings__status=Booking.STATUS_CANCELLED),
            )
        )
        .order_by('starts_at')
    )
    if service_id:
        qs = qs.filter(service_id=service_id)
    if day is not None:
        start = timezone.make_aware(datetime.combine(day.date(), time.min))
        end = start + timedelta(days=1)
        qs = qs.filter(starts_at__gte=start, starts_at__lt=end)
    return [s for s in qs if s.capacity > s.active_bookings]


@require_http_methods(['GET', 'POST'])
def booking_page(request):
    services = BookingService.objects.filter(is_active=True).order_by('sort_order', 'title')
    form = BookingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        slot = form.cleaned_data['slot']
        try:
            with transaction.atomic():
                locked = BookingSlot.objects.select_for_update().get(pk=slot.pk)
                if locked.seats_left <= 0 or locked.starts_at < timezone.now():
                    raise forms.ValidationError(_('Слот недоступний'))
                booking = Booking.objects.create(
                    slot=locked,
                    user=request.user if request.user.is_authenticated else None,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data.get('email') or '',
                    comment=form.cleaned_data.get('comment') or '',
                    status=Booking.STATUS_NEW,
                )
            _notify_booking(booking)
            messages.success(request, _('Бронювання прийнято. Очікуйте підтвердження.'))
            return redirect('booking:page')
        except forms.ValidationError as exc:
            messages.error(request, exc.message)
        except Exception:
            logger.exception('Booking create failed')
            messages.error(request, _('Не вдалося створити бронювання'))
    return render(request, 'booking/page.html', {
        'form': form,
        'services': services,
    })


@require_GET
def booking_slots_partial(request):
    service_id = request.GET.get('service') or None
    date_str = request.GET.get('date') or ''
    day = None
    if date_str:
        try:
            day = timezone.make_aware(datetime.strptime(date_str, '%Y-%m-%d'))
        except ValueError:
            day = None
    slots = _available_slots(int(service_id) if service_id else None, day)
    return render(request, 'booking/partials/slots.html', {'slots': slots})


@require_POST
def booking_request(request):
    """Compat endpoint: redirect home form to full booking page if no slot."""
    if request.POST.get('slot'):
        form = BookingForm(request.POST)
        if form.is_valid():
            slot = form.cleaned_data['slot']
            with transaction.atomic():
                locked = BookingSlot.objects.select_for_update().get(pk=slot.pk)
                if locked.seats_left <= 0:
                    messages.error(request, _('Немає вільних місць'))
                    return _redirect_next(request)
                booking = Booking.objects.create(
                    slot=locked,
                    user=request.user if request.user.is_authenticated else None,
                    name=form.cleaned_data['name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data.get('email') or '',
                    comment=form.cleaned_data.get('comment') or '',
                    status=Booking.STATUS_NEW,
                )
            _notify_booking(booking)
            messages.success(request, _('Бронювання прийнято.'))
            return _redirect_next(request)
        messages.error(request, _('Перевірте дані бронювання.'))
        return _redirect_next(request)
    messages.info(request, _('Оберіть послугу та час на сторінці бронювання.'))
    return redirect('booking:page')
