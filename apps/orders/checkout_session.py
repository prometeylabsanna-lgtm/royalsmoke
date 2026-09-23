"""Sliding checkout session + expiry warning."""

from __future__ import annotations

import time

from django.conf import settings

CHECKOUT_EXPIRES_AT_KEY = 'rs_checkout_expires_at'


def checkout_session_seconds() -> int:
    return int(getattr(settings, 'CHECKOUT_SESSION_SECONDS', 60 * 60))


def checkout_warn_seconds() -> int:
    return int(getattr(settings, 'CHECKOUT_WARN_SECONDS', 5 * 60))


def touch_checkout_session(request) -> None:
    """Slide session expiry forward on checkout activity."""
    seconds = checkout_session_seconds()
    request.session.set_expiry(seconds)
    request.session[CHECKOUT_EXPIRES_AT_KEY] = time.time() + seconds
    request.session.modified = True


def checkout_expiry_context(request) -> dict:
    expires_at = request.session.get(CHECKOUT_EXPIRES_AT_KEY)
    if not expires_at:
        return {
            'checkout_expires_in': None,
            'checkout_show_warn': False,
            'checkout_warn_minutes': checkout_warn_seconds() // 60,
        }
    remaining = max(0, int(expires_at - time.time()))
    return {
        'checkout_expires_in': remaining,
        'checkout_show_warn': 0 < remaining <= checkout_warn_seconds(),
        'checkout_warn_minutes': max(1, (remaining + 59) // 60),
    }
