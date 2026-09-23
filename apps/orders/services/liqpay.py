"""LiqPay payment helpers (data/signature + callback verify)."""

from __future__ import annotations

import base64
import hashlib
import json
import logging
from decimal import Decimal
from typing import Any

from django.conf import settings
from django.utils.translation import get_language

logger = logging.getLogger(__name__)

LIQPAY_CHECKOUT_URL = 'https://www.liqpay.ua/api/3/checkout'


def _keys() -> tuple[str, str]:
    pub = (getattr(settings, 'LIQPAY_PUBLIC_KEY', '') or '').strip()
    priv = (getattr(settings, 'LIQPAY_PRIVATE_KEY', '') or '').strip()
    return pub, priv


def _encode(payload: dict) -> str:
    raw = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return base64.b64encode(raw).decode('ascii')


def _sign(data_b64: str, private_key: str) -> str:
    digest = hashlib.sha1(
        (private_key + data_b64 + private_key).encode('utf-8')
    ).digest()
    return base64.b64encode(digest).decode('ascii')


def create_checkout_payload(
    order,
    *,
    result_url: str,
    server_url: str,
    description: str | None = None,
) -> dict[str, str]:
    public_key, private_key = _keys()
    if not public_key or not private_key:
        raise ValueError('LiqPay keys are not configured')
    sandbox = getattr(settings, 'LIQPAY_SANDBOX', True)
    from apps.core.money import money, reconcile_order_totals
    if hasattr(order, 'items'):
        reconcile_order_totals(order)
    amount = money(order.total)
    lang = (get_language() or 'uk').lower()
    liqpay_lang = 'uk' if lang.startswith('uk') else 'en'
    payload: dict[str, Any] = {
        'public_key': public_key,
        'version': 3,
        'action': 'pay',
        'amount': float(amount),
        'currency': order.currency or 'UAH',
        'description': description or f'Order {order.order_number}',
        'order_id': order.order_number,
        'result_url': result_url,
        'server_url': server_url,
        'language': liqpay_lang,
    }
    if sandbox:
        payload['sandbox'] = 1
    data = _encode(payload)
    signature = _sign(data, private_key)
    return {
        'data': data,
        'signature': signature,
        'checkout_url': LIQPAY_CHECKOUT_URL,
    }


def verify_callback(data: str, signature: str) -> dict[str, Any]:
    _, private_key = _keys()
    if not private_key:
        raise ValueError('LiqPay private key is not configured')
    expected = _sign(data, private_key)
    if not signature or expected != signature:
        logger.warning('LiqPay signature mismatch')
        raise ValueError('Invalid LiqPay signature')
    raw = base64.b64decode(data.encode('ascii'))
    return json.loads(raw.decode('utf-8'))
