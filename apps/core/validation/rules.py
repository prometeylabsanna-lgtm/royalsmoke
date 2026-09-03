"""Чисті правила валідації. Повертають текст помилки або None."""

from __future__ import annotations

import re
from typing import Optional

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from apps.core.validation import messages as msg

# Літери (латиниця + кирилиця UA/RU), пробіл, дефіс, апострофи
NAME_RE = re.compile(
    r"^[A-Za-zА-Яа-яЁёІіЇїЄєҐґ'ʼ\- ]+$",
)

# Практичний RFC 5321/5322-сумісний патерн для типових адрес
EMAIL_RE = re.compile(
    r"^(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
    r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|'
    r'\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@'
    r'(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
    r'[a-zA-Z]{2,}|'
    r'\[(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}'
    r'(?:25[0-5]|2[0-4]\d|[01]?\d\d?|[a-zA-Z\-0-9]*[a-zA-Z0-9]:'
    r'(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|'
    r'\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])$'
)

# Міжнародний телефон: опційний +, цифри та роздільники; ≥7 цифр
PHONE_RE = re.compile(r'^\+?[\d\s\-()./]{7,25}$')
PHONE_DIGITS_RE = re.compile(r'\d')

SPECIAL_RE = re.compile(r'[^A-Za-z0-9]')

_url_validator = URLValidator()


def is_blank(value) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return False
    return str(value).strip() == ''


def validate_required(value, *, checkbox: bool = False) -> Optional[str]:
    if checkbox:
        if value is True or value == 'on' or value == '1' or value == 1:
            return None
        return msg.REQUIRED_CHECKBOX
    if value is None:
        return msg.REQUIRED
    if isinstance(value, str) and value.strip() == '':
        if value != '' and value.strip() == '':
            return msg.WHITESPACE
        return msg.REQUIRED
    return None


def validate_name(value) -> Optional[str]:
    text = str(value).strip()
    if len(text) < 2:
        return msg.NAME_MIN
    if not NAME_RE.match(text):
        return msg.NAME_CHARS
    return None


def validate_email(value) -> Optional[str]:
    text = str(value).strip()
    if len(text) > 254 or not EMAIL_RE.match(text):
        return msg.EMAIL
    return None


def validate_password(value) -> Optional[str]:
    text = str(value)
    if len(text) < 8:
        return msg.PASSWORD_MIN
    if not re.search(r'[A-Z]', text):
        return msg.PASSWORD_UPPER
    if not re.search(r'[a-z]', text):
        return msg.PASSWORD_LOWER
    if not re.search(r'\d', text):
        return msg.PASSWORD_DIGIT
    if not SPECIAL_RE.search(text):
        return msg.PASSWORD_SPECIAL
    return None


def validate_phone(value) -> Optional[str]:
    text = str(value).strip()
    if not PHONE_RE.match(text):
        return msg.PHONE
    digits = PHONE_DIGITS_RE.findall(text)
    if len(digits) < 7 or len(digits) > 15:
        return msg.PHONE
    return None


def validate_url(value) -> Optional[str]:
    text = str(value).strip()
    if text.startswith('/') and not text.startswith('//'):
        # Внутрішні шляхи CMS (наприклад /catalog/)
        if len(text) > 1 or text == '/':
            return None
    try:
        _url_validator(text)
    except DjangoValidationError:
        return msg.URL
    return None


RULES = {
    'required': validate_required,
    'name': validate_name,
    'email': validate_email,
    'password': validate_password,
    'phone': validate_phone,
    'url': validate_url,
}


def run_rule(rule: str, value, *, optional: bool = False, checkbox: bool = False) -> Optional[str]:
    """Застосувати правило. Optional: порожнє значення — OK."""
    if rule == 'required':
        return validate_required(value, checkbox=checkbox)
    if optional and is_blank(value):
        return None
    if not optional:
        err = validate_required(value, checkbox=checkbox)
        if err:
            return err
    fn = RULES.get(rule)
    if fn is None:
        return None
    if rule == 'required':
        return fn(value, checkbox=checkbox)
    return fn(value)
