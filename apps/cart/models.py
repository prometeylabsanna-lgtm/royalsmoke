from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'

    def __str__(self) -> str:
        return f'Cart<{self.user_id}>'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиція кошика'
        verbose_name_plural = 'Позиції кошика'
        constraints = [
            models.UniqueConstraint(fields=('cart', 'product'), name='uniq_cart_product'),
        ]

    def __str__(self) -> str:
        return f'{self.product_id} x{self.quantity}'


class CartReservation(models.Model):
    """Soft hold on stock while a line sits in a guest/user cart."""

    product = models.ForeignKey(
        'catalog.Product',
        on_delete=models.CASCADE,
        related_name='cart_reservations',
    )
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='cart_reservations',
    )
    expires_at = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Резерв кошика'
        verbose_name_plural = 'Резерви кошика'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1),
                name='cart_reservation_qty_gte_1',
            ),
        ]
        indexes = [
            models.Index(fields=['product', 'expires_at']),
        ]

    def __str__(self) -> str:
        holder = self.user_id or self.session_key or '?'
        return f'Reserve<{self.product_id} x{self.quantity} @{holder}>'
