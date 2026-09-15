"""Unified admin/user notifications (email + Telegram)."""

from __future__ import annotations

import logging
import re
from typing import Iterable

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.core.services import telegram as tg

logger = logging.getLogger(__name__)

_EMAIL_SPLIT = re.compile(r'[\s,;]+')


def _admin_emails() -> list[str]:
    emails: list[str] = []
    try:
        from apps.core.models import SiteSettings

        raw = (SiteSettings.load().notify_emails or '').strip()
        if raw:
            emails.extend(e for e in _EMAIL_SPLIT.split(raw) if e and '@' in e)
    except Exception:
        logger.exception('Failed to load SiteSettings.notify_emails')
    if not emails:
        fallback = getattr(settings, 'NOTIFY_EMAIL', '') or ''
        if fallback:
            emails.append(fallback)
    # dedupe preserve order
    seen: set[str] = set()
    out: list[str] = []
    for e in emails:
        key = e.lower()
        if key not in seen:
            seen.add(key)
            out.append(e)
    return out


def _admin_telegram_chat_id() -> str:
    try:
        from apps.core.models import SiteSettings

        return (SiteSettings.load().telegram_notify_chat_id or '').strip()
    except Exception:
        logger.exception('Failed to load telegram_notify_chat_id')
        return ''


def _send_email(
    subject: str,
    text: str,
    recipients: Iterable[str],
    *,
    html: str | None = None,
) -> bool:
    to = [r for r in recipients if r]
    if not to:
        return False
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to,
        )
        if html:
            msg.attach_alternative(html, 'text/html')
        msg.send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Email send failed to %s', to)
        return False


def notify_admins(
    subject: str,
    text: str,
    *,
    html: str | None = None,
    telegram_text: str | None = None,
) -> None:
    _send_email(subject, text, _admin_emails(), html=html)
    chat_id = _admin_telegram_chat_id()
    if chat_id:
        tg.send_message(chat_id, telegram_text or f'{subject}\n\n{text}')


def notify_user(
    email: str | None,
    subject: str,
    text: str,
    *,
    html: str | None = None,
    user=None,
    telegram_text: str | None = None,
) -> None:
    send_email = True
    if user is not None and hasattr(user, 'notify_email'):
        send_email = bool(user.notify_email)
    if send_email and email:
        _send_email(subject, text, [email], html=html)

    if user is not None and getattr(user, 'notify_telegram', False):
        chat_id = (getattr(user, 'telegram_chat_id', '') or '').strip()
        if chat_id:
            tg.send_message(chat_id, telegram_text or f'{subject}\n\n{text}')


def render_email(template_base: str, context: dict) -> tuple[str, str | None]:
    """Return (text, html) from templates/emails/{base}.txt and .html."""
    text = render_to_string(f'emails/{template_base}.txt', context)
    html = None
    try:
        html = render_to_string(f'emails/{template_base}.html', context)
    except Exception:
        pass
    return text, html
