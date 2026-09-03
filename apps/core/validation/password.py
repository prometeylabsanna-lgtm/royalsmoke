"""Django AUTH_PASSWORD_VALIDATORS — посилені правила Royal Smoke."""

from __future__ import annotations

from django.core.exceptions import ValidationError

from apps.core.validation.rules import validate_password


class StrongPasswordValidator:
    """Мін. 8 символів, велика/мала літера, цифра, спецсимвол."""

    def validate(self, password, user=None):
        err = validate_password(password or '')
        if err:
            raise ValidationError(err, code='password_too_weak')

    def get_help_text(self):
        return (
            'Пароль має містити мінімум 8 символів, велику та малу літери, '
            'цифру та спеціальний символ.'
        )
