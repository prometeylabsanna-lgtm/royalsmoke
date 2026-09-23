from __future__ import annotations

from decimal import Decimal

from django.core.cache import cache
from django.core.validators import MinValueValidator
from django.db import models


def clear_site_content_cache() -> None:
    from django.conf import settings

    cache.delete('site_settings')
    cache.delete('site_blocks')
    cache.delete('page_styles')
    for code, _name in settings.LANGUAGES:
        cache.delete(f'site_settings:{code}')
        cache.delete(f'site_blocks:{code}')


class SiteSettings(models.Model):
    """Singleton глобальних налаштувань (pk=1)."""

    site_name = models.CharField('Назва сайту', max_length=100, default='Royal Smoke')
    phone = models.CharField('Телефон', max_length=64, blank=True, default='+380 44 000 00 00')
    email = models.EmailField('Email', blank=True, default='hello@royalsmoke.ua')
    address = models.CharField('Адреса', max_length=255, blank=True, default='Київ, Україна')
    work_hours = models.CharField('Години роботи', max_length=255, blank=True, default='Пн–Нд: 11:00–21:00')
    instagram_url = models.URLField('Instagram', blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    notify_emails = models.TextField(
        'Email для сповіщень',
        blank=True,
        help_text='Адреси через кому або з нового рядка.',
    )
    telegram_notify_chat_id = models.CharField('Telegram канал/чат для лідів', max_length=64, blank=True)
    free_delivery_from = models.DecimalField(
        'Безкоштовна доставка від', max_digits=10, decimal_places=2, null=True, blank=True,
    )
    meta_description = models.TextField('SEO-опис головної', blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self) -> str:
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        clear_site_content_cache()

    def delete(self, *args, **kwargs):
        return None

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class CurrencyRate(models.Model):
    """Курс до гривні. 1 одиниця валюти = uah_per_unit гривень."""

    code = models.CharField(
        'Код ISO',
        max_length=3,
        unique=True,
        help_text='USD, CNY, EUR… Для нової мови додайте валюту тут і рядок у LANGUAGE_CURRENCY.',
    )
    name = models.CharField('Назва', max_length=64)
    symbol = models.CharField('Символ', max_length=8)
    uah_per_unit = models.DecimalField(
        'Гривень за 1 одиницю',
        max_digits=12,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))],
        help_text='Скільки гривень коштує 1 одиниця цієї валюти. Для UAH завжди 1.',
    )
    sort_order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Курс валюти'
        verbose_name_plural = 'Курси валют'
        ordering = ['sort_order', 'code']

    def __str__(self) -> str:
        return f'{self.code} ({self.symbol})'

    def save(self, *args, **kwargs):
        self.code = (self.code or '').upper()
        if self.code == 'UAH':
            self.uah_per_unit = 1
        super().save(*args, **kwargs)
        from apps.core.currency import clear_currency_cache

        clear_currency_cache()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        from apps.core.currency import clear_currency_cache

        clear_currency_cache()


class SiteBlock(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'
        URL = 'url', 'Посилання'
        VIDEO = 'video', 'Відео'

    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        SITE = 'site', 'Сайт'
        CATALOG = 'catalog', 'Каталог'
        SERVICE = 'service', 'Сервіс'
        ABOUT = 'about', 'Про нас'
        BLOG = 'blog', 'Блог'
        FAQ = 'faq', 'FAQ'
        CONTACT = 'contact', 'Контакти'
        DELIVERY = 'delivery', 'Доставка'
        B2B = 'b2b', 'B2B'
        BOOKING = 'booking', 'Бронювання'
        CART = 'cart', 'Кошик'
        CHECKOUT = 'checkout', 'Оформлення'
        CABINET = 'cabinet', 'Кабінет'
        AGE = 'age', 'Age gate'

    page = models.CharField(max_length=32, choices=Page.choices, verbose_name='Сторінка')
    key = models.CharField(max_length=64, verbose_name='Ключ блоку')
    label = models.CharField(max_length=128, verbose_name='Назва в адмінці')
    content_type = models.CharField(
        max_length=16, choices=ContentType.choices, default=ContentType.TEXT,
    )
    text_html = models.TextField(blank=True, verbose_name='Текст')
    image = models.ImageField(upload_to='blocks/', blank=True, verbose_name='Зображення')
    link_url = models.CharField('URL посилання', max_length=512, blank=True)
    link_label = models.CharField('Текст посилання', max_length=128, blank=True)
    video_embed_url = models.URLField('URL відео (YouTube/Vimeo)', blank=True)
    video_file = models.FileField('Відеофайл', upload_to='blocks/video/', blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['page', 'sort_order', 'key']
        verbose_name = 'Блок контенту'
        verbose_name_plural = 'Блоки контенту'
        constraints = [
            models.UniqueConstraint(fields=['page', 'key'], name='unique_rs_site_block_page_key'),
        ]

    def __str__(self) -> str:
        return f'{self.page}.{self.key}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        clear_site_content_cache()

    @property
    def cache_key(self) -> str:
        return f'{self.page}.{self.key}'


class PageStyle(models.Model):
    """Колір фону окремої сторінки. Порожній background_color = дефолт сайту."""

    DEFAULT_BACKGROUND = '#100d0c'

    page = models.CharField(
        'Сторінка',
        max_length=32,
        choices=SiteBlock.Page.choices,
        unique=True,
    )
    background_color = models.CharField(
        'Колір фону',
        max_length=32,
        blank=True,
        help_text='HEX (#100d0c). Порожнє значення — дефолтний стиль сайту.',
    )

    class Meta:
        ordering = ['page']
        verbose_name = 'Стиль сторінки'
        verbose_name_plural = 'Стилі сторінок'

    def __str__(self) -> str:
        return f'{self.get_page_display()}: {self.effective_color}'

    @property
    def is_custom(self) -> bool:
        return bool((self.background_color or '').strip())

    @property
    def effective_color(self) -> str:
        raw = (self.background_color or '').strip()
        return raw or self.DEFAULT_BACKGROUND

    def reset_to_default(self) -> None:
        self.background_color = ''
        self.save(update_fields=['background_color'])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        clear_site_content_cache()


class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=255, blank=True)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    image = models.ImageField('Фото', upload_to='hero/', blank=True)
    cta_primary_label = models.CharField('Основна кнопка', max_length=80, blank=True, default='До каталогу')
    cta_primary_url = models.CharField('URL основної кнопки', max_length=255, blank=True, default='/catalog/')
    cta_secondary_label = models.CharField('Другорядна кнопка', max_length=80, blank=True, default='Сигари')
    cta_secondary_url = models.CharField('URL другорядної кнопки', max_length=255, blank=True, default='/catalog/cigars/')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Слайд банера'
        verbose_name_plural = 'Слайди банера'

    def __str__(self) -> str:
        return self.title or f'Слайд #{self.pk or "новий"}'


class HistorySlide(models.Model):
    year_label = models.CharField('Рік / мітка', max_length=40)
    title = models.CharField('Заголовок', max_length=255, blank=True)
    text = models.TextField('Текст', blank=True)
    image = models.ImageField('Фото', upload_to='history/', blank=True)
    cta_label = models.CharField('Текст кнопки', max_length=80, blank=True, default='Читати далі')
    cta_url = models.CharField('URL кнопки', max_length=255, blank=True, default='/about/')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Слайд історії'
        verbose_name_plural = 'Слайди історії'

    def __str__(self) -> str:
        return f'{self.year_label}: {self.title}' if self.title else self.year_label


class HomeBrandCard(models.Model):
    brand = models.ForeignKey(
        'catalog.Brand',
        on_delete=models.CASCADE,
        related_name='home_cards',
        verbose_name='Бренд',
    )
    image = models.ImageField('Фото картки', upload_to='home_brands/', blank=True)
    text = models.TextField('Текст на картці', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Картка бренду на головній'
        verbose_name_plural = 'Картки брендів на головній'

    def __str__(self) -> str:
        return str(self.brand_id and self.brand) or f'Картка #{self.pk or "нова"}'


from apps.core.models_proxies import *  # noqa: E402,F401,F403
