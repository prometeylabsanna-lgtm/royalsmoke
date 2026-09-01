from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.booking.models import Booking, BookingService, BookingSlot


class BookingForm(forms.Form):
    """Legacy slot-based booking (admin / optional full page)."""

    service = forms.ModelChoiceField(label='Послуга', queryset=BookingService.objects.none())
    slot = forms.ModelChoiceField(label='Слот', queryset=BookingSlot.objects.none())
    name = forms.CharField(label='Імʼя', max_length=120)
    phone = forms.CharField(label='Телефон', max_length=30)
    email = forms.EmailField(label='Email', required=False)
    comment = forms.CharField(label='Коментар', required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].queryset = BookingService.objects.filter(is_active=True)
        from django.utils import timezone
        now = timezone.now()
        self.fields['slot'].queryset = BookingSlot.objects.filter(
            is_active=True, starts_at__gte=now,
        ).select_related('service')


class BookingRequestForm(forms.Form):
    """Simplified contact booking: name + phone + wishes."""

    name = forms.CharField(label='Імʼя', max_length=120)
    phone = forms.CharField(label='Телефон', max_length=30)
    comment = forms.CharField(label='Побажання', required=False, max_length=500)


def _notify_booking(booking: Booking) -> None:
    slot_label = str(booking.slot) if booking.slot_id else 'без слоту (запит)'
    send_mail(
        f'Нове бронювання #{booking.pk}',
        (
            f'{booking.name}\n'
            f'{booking.phone}\n'
            f'{booking.email or "—"}\n'
            f'{slot_label}\n'
            f'{booking.comment or ""}'
        ),
        settings.DEFAULT_FROM_EMAIL,
        [settings.NOTIFY_EMAIL],
        fail_silently=True,
    )


def _redirect_next(request, fallback: str = 'booking:page'):
    next_url = request.POST.get('next') or ''
    if next_url.startswith('/'):
        return redirect(next_url)
    return redirect(fallback)


@require_POST
def booking_request(request):
    form = BookingRequestForm(request.POST)
    if form.is_valid():
        booking = Booking.objects.create(
            slot=None,
            user=request.user if request.user.is_authenticated else None,
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            email='',
            comment=form.cleaned_data.get('comment') or '',
            status=Booking.STATUS_NEW,
        )
        _notify_booking(booking)
        messages.success(request, 'Заявку прийнято. Менеджер звʼяжеться з вами.')
    else:
        messages.error(request, 'Перевірте імʼя та телефон.')
    return _redirect_next(request)


@require_http_methods(['GET', 'POST'])
def booking_page(request):
    form = BookingRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = Booking.objects.create(
            slot=None,
            user=request.user if request.user.is_authenticated else None,
            name=form.cleaned_data['name'],
            phone=form.cleaned_data['phone'],
            email='',
            comment=form.cleaned_data.get('comment') or '',
            status=Booking.STATUS_NEW,
        )
        _notify_booking(booking)
        messages.success(request, 'Заявку прийнято. Менеджер звʼяжеться з вами.')
        return _redirect_next(request)
    return render(request, 'booking/booking.html', {
        'form': form,
    })
