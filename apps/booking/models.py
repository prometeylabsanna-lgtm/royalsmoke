from django.conf import settings
from django.db import models
from django.utils import timezone


class BookingService(models.Model):
    class Kind(models.TextChoices):
        TASTING = 'tasting', 'Дегустація'
        CONSULTATION = 'consultation', 'Консультація сомельє'
        SHOWROOM = 'showroom', 'Візит у шоурум'
        PICKUP = 'pickup', 'Самовивіз'

    kind = models.CharField('Тип', max_length=32, choices=Kind.choices, unique=True)
    title = models.CharField('Назва', max_length=160)
    description = models.TextField('Опис', blank=True)
    duration_minutes = models.PositiveIntegerField('Тривалість, хв', default=60)
    capacity = models.PositiveIntegerField('Місць на слот', default=1)
    is_active = models.BooleanField('Активна', default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Послуга бронювання'
        verbose_name_plural = 'Послуги бронювання'
        ordering = ['sort_order', 'title']

    def __str__(self) -> str:
        return self.title


class BookingSlot(models.Model):
    service = models.ForeignKey(BookingService, on_delete=models.CASCADE, related_name='slots')
    starts_at = models.DateTimeField('Початок')
    ends_at = models.DateTimeField('Кінець')
    capacity = models.PositiveIntegerField('Місткість', default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Слот'
        verbose_name_plural = 'Слоти'
        ordering = ['starts_at']
        indexes = [models.Index(fields=['starts_at', 'is_active'])]

    def __str__(self) -> str:
        return f'{self.service.title} · {timezone.localtime(self.starts_at):%d.%m %H:%M}'

    @property
    def booked_count(self) -> int:
        return self.bookings.exclude(status=Booking.STATUS_CANCELLED).count()

    @property
    def seats_left(self) -> int:
        return max(0, self.capacity - self.booked_count)


class Booking(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Нове'),
        (STATUS_CONFIRMED, 'Підтверджено'),
        (STATUS_DONE, 'Завершено'),
        (STATUS_CANCELLED, 'Скасовано'),
    ]

    slot = models.ForeignKey(
        BookingSlot,
        on_delete=models.PROTECT,
        related_name='bookings',
        null=True,
        blank=True,
        verbose_name='Слот',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='bookings',
    )
    name = models.CharField('Імʼя', max_length=120)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank=True, default='')
    comment = models.TextField('Коментар', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-created_at']

    def __str__(self) -> str:
        if self.slot_id:
            return f'{self.name} · {self.slot}'
        return f'{self.name} · запит'
