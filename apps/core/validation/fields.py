"""Django form fields з єдиними правилами валідації."""

from __future__ import annotations

from django import forms
from django.core.exceptions import ValidationError

from apps.core.validation import messages as msg
from apps.core.validation.rules import (
    validate_email,
    validate_name,
    validate_password,
    validate_phone,
    validate_url,
)


def _attrs(rule: str, optional: bool = False, extra: dict | None = None) -> dict:
    attrs = {
        'data-rs-rule': rule,
    }
    if optional:
        attrs['data-rs-optional'] = '1'
    if extra:
        attrs.update(extra)
    return attrs


def _required_messages() -> dict:
    return {'required': msg.REQUIRED}


class NameField(forms.CharField):
    def __init__(self, *args, optional: bool = False, **kwargs):
        kwargs.setdefault('max_length', 120)
        kwargs.setdefault('required', not optional)
        kwargs.setdefault('error_messages', _required_messages())
        widget = kwargs.get('widget') or forms.TextInput()
        if hasattr(widget, 'attrs'):
            widget.attrs.update(_attrs('name', optional=optional))
        kwargs['widget'] = widget
        self._optional = optional
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if self._optional and (value is None or str(value).strip() == ''):
            return ''
        err = validate_name(value)
        if err:
            raise ValidationError(err)
        return str(value).strip()


class EmailField(forms.CharField):
    def __init__(self, *args, optional: bool = False, **kwargs):
        kwargs.setdefault('max_length', 254)
        kwargs.setdefault('required', not optional)
        kwargs.setdefault('error_messages', _required_messages())
        widget = kwargs.get('widget') or forms.EmailInput()
        if hasattr(widget, 'attrs'):
            widget.attrs.update(_attrs('email', optional=optional))
        kwargs['widget'] = widget
        self._optional = optional
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if self._optional and (value is None or str(value).strip() == ''):
            return ''
        err = validate_email(value)
        if err:
            raise ValidationError(err)
        return str(value).strip()


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', True)
        kwargs.setdefault('strip', False)
        kwargs.setdefault('error_messages', _required_messages())
        widget = kwargs.get('widget') or forms.PasswordInput()
        if hasattr(widget, 'attrs'):
            widget.attrs.update(_attrs('password'))
        kwargs['widget'] = widget
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        err = validate_password(value)
        if err:
            raise ValidationError(err)
        return value


class PhoneField(forms.CharField):
    def __init__(self, *args, optional: bool = False, **kwargs):
        kwargs.setdefault('max_length', 30)
        kwargs.setdefault('required', not optional)
        kwargs.setdefault('error_messages', _required_messages())
        widget = kwargs.get('widget') or forms.TextInput(attrs={'type': 'tel'})
        if hasattr(widget, 'attrs'):
            widget.attrs.update(_attrs('phone', optional=optional))
            widget.attrs.setdefault('type', 'tel')
        kwargs['widget'] = widget
        self._optional = optional
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if self._optional and (value is None or str(value).strip() == ''):
            return ''
        err = validate_phone(value)
        if err:
            raise ValidationError(err)
        return str(value).strip()


class UrlField(forms.CharField):
    """URL або внутрішній шлях (/catalog/)."""

    def __init__(self, *args, optional: bool = False, **kwargs):
        kwargs.setdefault('max_length', 255)
        kwargs.setdefault('required', not optional)
        kwargs.setdefault('error_messages', _required_messages())
        widget = kwargs.get('widget') or forms.TextInput()
        if hasattr(widget, 'attrs'):
            widget.attrs.update(_attrs('url', optional=optional))
        kwargs['widget'] = widget
        self._optional = optional
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        if self._optional and (value is None or str(value).strip() == ''):
            return ''
        err = validate_url(value)
        if err:
            raise ValidationError(err)
        return str(value).strip()


class RequiredCheckboxField(forms.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', True)
        kwargs.setdefault('error_messages', {'required': msg.REQUIRED_CHECKBOX})
        widget = kwargs.get('widget') or forms.CheckboxInput()
        if hasattr(widget, 'attrs'):
            widget.attrs.update({'data-rs-rule': 'required', 'data-rs-checkbox': '1'})
        kwargs['widget'] = widget
        super().__init__(*args, **kwargs)
