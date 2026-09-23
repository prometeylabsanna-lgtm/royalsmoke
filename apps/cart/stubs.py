"""Placeholder product when a cart SKU was deleted from the catalog."""

from __future__ import annotations

from decimal import Decimal

from django.utils.translation import gettext_lazy as _


class _EmptyImages:
    def all(self):
        return []


class MissingProduct:
    """Duck-typed stand-in so cart/checkout templates never 500."""

    def __init__(self, product_id: int):
        self.id = int(product_id)
        self.pk = self.id
        self.name = str(_('Товар недоступний'))
        self.base_price = Decimal('0')
        self.old_price = None
        self.stock = 0
        self.is_active = False
        self.sku = ''
        self.brand = None
        self.images = _EmptyImages()
        self._missing = True

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return '#'

    @property
    def display_price(self):
        return self.base_price

    def available_stock(self) -> int:
        return 0
