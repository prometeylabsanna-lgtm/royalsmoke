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
    variant = models.ForeignKey(
        'catalog.ProductVariant', null=True, blank=True, on_delete=models.SET_NULL,
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиція кошика'
        verbose_name_plural = 'Позиції кошика'

    def __str__(self) -> str:
        return f'{self.product_id} x{self.quantity}'
