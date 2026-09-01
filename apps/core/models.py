from __future__ import annotations

from django.core.cache import cache
from django.db import models


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
    meta_description = models.TextField('Meta description головної', blank=True)

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self) -> str:
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete('site_settings')

    def delete(self, *args, **kwargs):
        return None

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteBlock(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Фото'

    class Page(models.TextChoices):
        HOME = 'home', 'Головна'
        SITE = 'site', 'Сайт'
        CATALOG = 'catalog', 'Каталог'
        SERVICE = 'service', 'Сервіс'

    page = models.CharField(max_length=32, choices=Page.choices, verbose_name='Сторінка')
    key = models.CharField(max_length=64, verbose_name='Ключ блоку')
    label = models.CharField(max_length=128, verbose_name='Назва в адмінці')
    content_type = models.CharField(
        max_length=16, choices=ContentType.choices, default=ContentType.TEXT,
    )
    text_html = models.TextField(blank=True, verbose_name='Текст')
    image = models.ImageField(upload_to='blocks/', blank=True, verbose_name='Зображення')
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
        cache.delete('site_blocks')


class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=255, blank=True)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    image = models.ImageField('Фото', upload_to='hero/', blank=True)
    cta_primary_label = models.CharField('CTA primary', max_length=80, blank=True, default='До каталогу')
    cta_primary_url = models.CharField('CTA primary URL', max_length=255, blank=True, default='/catalog/')
    cta_secondary_label = models.CharField('CTA secondary', max_length=80, blank=True, default='Сигари')
    cta_secondary_url = models.CharField('CTA secondary URL', max_length=255, blank=True, default='/catalog/cigars/')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Слайд hero'
        verbose_name_plural = 'Слайди hero'

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


# --- CMS proxy sections (sidebar slots) ---

class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Hero'
        verbose_name_plural = 'Головна — Hero'


class HomeCategoriesSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Категорії'
        verbose_name_plural = 'Головна — Категорії'


class HomeTopSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Топ продажів'
        verbose_name_plural = 'Головна — Топ продажів'


class HomeNewSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Новинки'
        verbose_name_plural = 'Головна — Новинки'


class HomeAboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Історія сигар'
        verbose_name_plural = 'Головна — Історія сигар'


class HomeServiceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головна — Сервіс'
        verbose_name_plural = 'Головна — Сервіс'


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Меню / Header'
        verbose_name_plural = 'Меню / Header'


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Footer'
        verbose_name_plural = 'Footer'
