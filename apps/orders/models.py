import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_AWAITING_PAYMENT = 'awaiting_payment'
    STATUS_PAID = 'paid'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Нове')),
        (STATUS_AWAITING_PAYMENT, _('Очікує оплату')),
        (STATUS_PAID, _('Оплачено')),
        (STATUS_PROCESSING, _('В обробці')),
        (STATUS_SHIPPED, _('Відправлено')),
        (STATUS_DONE, _('Виконано')),
        (STATUS_CANCELLED, _('Скасовано')),
    ]

    PAYMENT_ONLINE = 'online'
    PAYMENT_COD = 'cod'
    PAYMENT_BANK = 'bank_transfer'
    PAYMENT_CHOICES = [
        (PAYMENT_ONLINE, _('Онлайн оплата')),
        (PAYMENT_COD, _('Оплата при отриманні')),
        (PAYMENT_BANK, _('Безготівковий розрахунок')),
    ]

    DELIVERY_NP = 'nova_poshta'
    DELIVERY_COURIER = 'courier'
    DELIVERY_PICKUP = 'pickup'
    DELIVERY_CHOICES = [
        (DELIVERY_NP, _('Нова Пошта')),
        (DELIVERY_COURIER, _('Курʼєр')),
        (DELIVERY_PICKUP, _('Самовивіз')),
    ]

    order_number = models.CharField('Номер', max_length=24, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='orders',
    )
    first_name = models.CharField('Імʼя', max_length=100)
    last_name = models.CharField('Прізвище', max_length=100)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email')
    comment = models.TextField('Коментар', blank=True)
    delivery_service = models.CharField('Доставка', max_length=20, choices=DELIVERY_CHOICES)
    delivery_city = models.CharField('Місто', max_length=150)
    delivery_address = models.CharField('Адреса / відділення', max_length=255)
    payment_method = models.CharField(
        'Оплата', max_length=20, choices=PAYMENT_CHOICES, default=PAYMENT_COD,
    )
    subtotal = models.DecimalField('Сума товарів', max_digits=12, decimal_places=2)
    discount = models.DecimalField('Знижка', max_digits=12, decimal_places=2, default=0)
    delivery_cost = models.DecimalField('Доставка', max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField('Разом', max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='UAH')
    market = models.CharField(max_length=8, default='UA')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    idempotency_key = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'RS{uuid.uuid4().hex[:8].upper()}'
        if not self.idempotency_key:
            self.idempotency_key = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('orders:thank_you', kwargs={'order_number': self.order_number})


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT)
    variant = models.ForeignKey(
        'catalog.ProductVariant', null=True, blank=True, on_delete=models.SET_NULL,
    )
    product_name = models.CharField(max_length=300)
    variant_name = models.CharField(max_length=120, blank=True)
    product_sku = models.CharField(max_length=80, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Позиція'
        verbose_name_plural = 'Позиції'

    def __str__(self) -> str:
        return self.product_name
