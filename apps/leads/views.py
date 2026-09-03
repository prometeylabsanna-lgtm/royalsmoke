from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.core.validation import EmailField, NameField, PhoneField
from apps.leads.models import Lead


class B2BForm(forms.Form):
    name = NameField(label='Контактна особа')
    company = forms.CharField(label='Компанія', max_length=160)
    phone = PhoneField(label='Телефон')
    email = EmailField(label='Email')
    message = forms.CharField(label='Запит', widget=forms.Textarea(attrs={'rows': 4}))


class ContactForm(forms.Form):
    name = NameField(label='Імʼя')
    phone = PhoneField(label='Телефон', optional=True)
    email = EmailField(label='Email', optional=True)
    message = forms.CharField(label='Повідомлення', widget=forms.Textarea(attrs={'rows': 4}))


class CallbackForm(forms.Form):
    name = NameField(label='Імʼя', optional=True)
    phone = PhoneField(label='Телефон')


def _notify(lead: Lead) -> None:
    send_mail(
        f'[{lead.get_kind_display()}] новий лід',
        f'{lead.name}\n{lead.phone}\n{lead.email}\n{lead.company}\n{lead.message}',
        settings.DEFAULT_FROM_EMAIL,
        [settings.NOTIFY_EMAIL],
        fail_silently=True,
    )


@require_http_methods(['GET', 'POST'])
def b2b_page(request):
    form = B2BForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        lead = Lead.objects.create(
            kind=Lead.Kind.B2B,
            name=data['name'],
            company=data['company'],
            phone=data['phone'],
            email=data['email'],
            message=data['message'],
            source_url=request.path,
        )
        _notify(lead)
        messages.success(request, 'Запит надіслано. Менеджер звʼяжеться з вами.')
        next_url = request.POST.get('next') or ''
        if next_url.startswith('/'):
            return redirect(next_url)
        return redirect('leads:b2b')
    return render(request, 'leads/b2b.html', {'form': form})


@require_http_methods(['GET'])
def delivery_page(request):
    return render(request, 'leads/delivery.html')


@require_http_methods(['GET', 'POST'])
def contact_page(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        lead = Lead.objects.create(
            kind=Lead.Kind.CONTACT,
            name=data['name'],
            phone=data.get('phone') or '',
            email=data.get('email') or '',
            message=data['message'],
            source_url=request.path,
        )
        _notify(lead)
        messages.success(request, 'Повідомлення надіслано.')
        return redirect('leads:contact')
    return render(request, 'leads/contact.html', {'form': form})


@require_http_methods(['POST'])
def callback(request):
    form = CallbackForm(request.POST)
    if form.is_valid():
        lead = Lead.objects.create(
            kind=Lead.Kind.CALLBACK,
            name=form.cleaned_data.get('name') or '',
            phone=form.cleaned_data['phone'],
            source_url=request.META.get('HTTP_REFERER', ''),
        )
        _notify(lead)
        if request.htmx:
            return HttpResponse(
                '<p class="form-success">Дякуємо! Передзвонимо найближчим часом.</p>'
            )
        messages.success(request, 'Заявку прийнято')
    elif request.htmx:
        return HttpResponse('<p class="form-error">Перевірте номер телефону.</p>', status=400)
    return redirect(request.META.get('HTTP_REFERER') or '/')
