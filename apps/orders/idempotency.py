"""Checkout / payment idempotency helpers."""

from __future__ import annotations

import hashlib
import hmac


def checkout_idempotency_key(token: str) -> str:
    """Stable unique key derived from one-time checkout token."""
    raw = (token or '').strip().encode('utf-8')
    return hashlib.sha256(b'rs-checkout:' + raw).hexdigest()


def tokens_match(expected: str | None, submitted: str | None) -> bool:
    if not expected or not submitted:
        return False
    return hmac.compare_digest(str(expected), str(submitted))
