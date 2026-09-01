from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обовʼязковий')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    preferred_language = models.CharField('Мова', max_length=10, default='uk')
    market = models.CharField('Ринок', max_length=8, default='UA')
    notify_email = models.BooleanField('Email-сповіщення', default=True)
    notify_telegram = models.BooleanField('Telegram-сповіщення', default=False)
    telegram_chat_id = models.CharField('Telegram chat id', max_length=64, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: list[str] = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self) -> str:
        return self.email


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    label = models.CharField('Назва', max_length=80, default='Основна')
    city = models.CharField('Місто', max_length=150)
    address = models.CharField('Адреса', max_length=255)
    is_default = models.BooleanField('За замовчуванням', default=False)

    class Meta:
        verbose_name = 'Адреса доставки'
        verbose_name_plural = 'Адреси доставки'

    def __str__(self) -> str:
        return f'{self.label}: {self.city}'


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Обране'
        verbose_name_plural = 'Обране'
