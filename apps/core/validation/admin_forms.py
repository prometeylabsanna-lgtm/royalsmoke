"""Форми CMS/адмінки з спільною валідацією."""

from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from apps.core.models import SiteSettings
from apps.core.validation.fields import EmailField, PhoneField, UrlField
from apps.core.validation.rules import validate_email


class SiteSettingsAdminForm(forms.ModelForm):
    phone = PhoneField(label='Телефон', optional=True)
    email = EmailField(label='Email', optional=True)
    instagram_url = UrlField(label='Instagram', optional=True)
    telegram_url = UrlField(label='Telegram', optional=True)
    facebook_url = UrlField(label='Facebook', optional=True)

    class Meta:
        model = SiteSettings
        fields = '__all__'

    def clean_notify_emails(self):
        raw = (self.cleaned_data.get('notify_emails') or '').strip()
        if not raw:
            return ''
        parts = [p.strip() for chunk in raw.replace(';', ',').split(',') for p in chunk.splitlines()]
        emails = [p for p in parts if p]
        for item in emails:
            err = validate_email(item)
            if err:
                raise ValidationError(f'{err}: {item}')
        return raw


def clean_optional_phone(value: str) -> str:
    from apps.core.validation.rules import validate_phone

    text = (value or '').strip()
    if not text:
        return ''
    err = validate_phone(text)
    if err:
        raise ValidationError(err)
    return text


def clean_optional_url(value: str) -> str:
    from apps.core.validation.rules import validate_url

    text = (value or '').strip()
    if not text:
        return ''
    err = validate_url(text)
    if err:
        raise ValidationError(err)
    return text
