"""Nova Poshta JSON API client."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from decimal import Decimal
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)

API_URL = 'https://api.novaposhta.ua/v2.0/json/'


class NovaPoshtaError(Exception):
    pass


def _api_key() -> str:
    return (getattr(settings, 'NOVA_POSHTA_API_KEY', '') or '').strip()


def call(model: str, method: str, properties: dict | None = None) -> list[dict]:
    key = _api_key()
    if not key:
        raise NovaPoshtaError('NOVA_POSHTA_API_KEY is not configured')
    payload = {
        'apiKey': key,
        'modelName': model,
        'calledMethod': method,
        'methodProperties': properties or {},
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode('utf-8'))
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        logger.exception('Nova Poshta request failed')
        raise NovaPoshtaError(str(exc)) from exc
    if not body.get('success'):
        errors = body.get('errors') or body.get('warnings') or ['Unknown NP error']
        raise NovaPoshtaError('; '.join(str(e) for e in errors))
    return body.get('data') or []


def search_cities(query: str, limit: int = 20) -> list[dict[str, str]]:
    q = (query or '').strip()
    if len(q) < 2:
        return []
    rows = call('Address', 'searchSettlements', {
        'CityName': q,
        'Limit': str(limit),
    })
    # searchSettlements wraps addresses
    out: list[dict[str, str]] = []
    for block in rows:
        for addr in block.get('Addresses') or []:
            out.append({
                'ref': addr.get('DeliveryCity') or addr.get('Ref') or '',
                'name': addr.get('Present') or addr.get('MainDescription') or '',
                'area': addr.get('Area') or '',
            })
    if out:
        return out
    # fallback getCities
    rows = call('Address', 'getCities', {'FindByString': q, 'Limit': str(limit)})
    for row in rows:
        out.append({
            'ref': row.get('Ref') or '',
            'name': row.get('Description') or '',
            'area': row.get('AreaDescription') or '',
        })
    return out


def get_warehouses(city_ref: str, query: str = '', limit: int = 50) -> list[dict[str, str]]:
    if not city_ref:
        return []
    props: dict[str, Any] = {
        'CityRef': city_ref,
        'Limit': str(limit),
    }
    if query.strip():
        props['FindByString'] = query.strip()
    rows = call('Address', 'getWarehouses', props)
    return [
        {
            'ref': r.get('Ref') or '',
            'name': r.get('Description') or '',
            'number': r.get('Number') or '',
            'address': r.get('ShortAddress') or r.get('Description') or '',
        }
        for r in rows
    ]


def calculate_delivery_cost(
    city_ref: str,
    *,
    weight_kg: Decimal | float = 1,
    cost: Decimal | float = 100,
) -> Decimal:
    sender_city = getattr(settings, 'NP_SENDER_CITY_REF', '') or ''
    if not sender_city or not city_ref:
        return Decimal('0')
    rows = call('InternetDocument', 'getDocumentPrice', {
        'CitySender': sender_city,
        'CityRecipient': city_ref,
        'Weight': str(weight_kg),
        'ServiceType': 'WarehouseWarehouse',
        'Cost': str(int(cost)),
        'CargoType': 'Cargo',
    })
    if not rows:
        return Decimal('0')
    price = rows[0].get('Cost') or rows[0].get('CostWarehouses') or 0
    return Decimal(str(price))


def create_ttn(order) -> dict[str, str]:
    """Create InternetDocument for order. Returns {ttn, ref}."""
    props = {
        'PayerType': 'Sender',
        'PaymentMethod': 'Cash',
        'DateTime': '',
        'CargoType': 'Cargo',
        'Weight': '1',
        'ServiceType': 'WarehouseWarehouse',
        'SeatsAmount': '1',
        'Description': f'Order {order.order_number}',
        'Cost': str(int(order.total)),
        'CitySender': getattr(settings, 'NP_SENDER_CITY_REF', ''),
        'Sender': getattr(settings, 'NP_SENDER_COUNTERPARTY_REF', '') or getattr(settings, 'NP_SENDER_REF', ''),
        'SenderAddress': getattr(settings, 'NP_SENDER_WAREHOUSE_REF', ''),
        'ContactSender': getattr(settings, 'NP_CONTACT_SENDER', '') or getattr(settings, 'NP_SENDER_CONTACT', ''),
        'SendersPhone': getattr(settings, 'NP_SENDER_PHONE', ''),
        'CityRecipient': order.np_city_ref,
        'RecipientAddress': order.np_warehouse_ref,
        'RecipientsPhone': order.phone,
        'RecipientName': f'{order.first_name} {order.last_name}'.strip(),
    }
    # Recipient counterparty often created via NewAddress recipient flow;
    # use simplified save for warehouse-warehouse with RecipientWarehouseIndex if needed.
    rows = call('InternetDocument', 'save', props)
    if not rows:
        raise NovaPoshtaError('Empty response from InternetDocument.save')
    row = rows[0]
    return {
        'ttn': row.get('IntDocNumber') or row.get('Number') or '',
        'ref': row.get('Ref') or '',
    }


def track_ttn(ttn: str) -> dict[str, Any]:
    rows = call('TrackingDocument', 'getStatusDocuments', {
        'Documents': [{'DocumentNumber': ttn}],
    })
    if not rows:
        return {}
    row = rows[0]
    return {
        'status_code': str(row.get('StatusCode') or ''),
        'status': row.get('Status') or '',
        'warehouse': row.get('WarehouseRecipient') or '',
        'raw': row,
    }
