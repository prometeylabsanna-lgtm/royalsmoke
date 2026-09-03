from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _lazy
from django.views.decorators.http import require_POST

from apps.booking.models import Booking
from apps.core.validation import NameField, PhoneField


class BookingRequestForm(forms.Form):
    """Simplified contact booking: name + phone + wishes."""

    name = NameField(label=_lazy('Імʼя'))
    phone = PhoneField(label=_lazy('Телефон'))
    comment = forms.CharField(label=_lazy('Побажання'), required=False, max_length=500)


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


def _redirect_next(request, fallback: str = 'pages:home'):
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
        messages.success(request, _('Заявку прийнято. Менеджер звʼяжеться з вами.'))
    else:
        messages.error(request, _('Перевірте імʼя та телефон.'))
    return _redirect_next(request)
