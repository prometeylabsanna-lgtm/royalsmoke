"""Thin Telegram Bot API client (server-side only)."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)

API_BASE = 'https://api.telegram.org'


def send_message(chat_id: str, text: str, *, parse_mode: str | None = None) -> bool:
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '') or ''
    if not token or not chat_id:
        return False
    payload: dict = {
        'chat_id': str(chat_id).strip(),
        'text': text[:4000],
        'disable_web_page_preview': True,
    }
    if parse_mode:
        payload['parse_mode'] = parse_mode
    url = f'{API_BASE}/bot{token}/sendMessage'
    data = urllib.parse.urlencode(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            ok = bool(body.get('ok'))
            if not ok:
                logger.warning('Telegram API rejected message: %s', body)
            return ok
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        logger.exception('Telegram send_message failed: %s', exc)
        return False
