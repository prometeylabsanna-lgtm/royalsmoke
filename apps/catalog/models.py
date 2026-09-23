from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.slug import unique_slug

from .models_base import Brand, Category, ProductLine, Tag, TimeStampedModel

_SLUG_HELP = 'Заповнюється автоматично з назви. Можна залишити порожнім.'


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def on_storefront(self):
        return self.active().filter(category__is_active=True, brand__is_active=True)

    def with_relations(self):
        return self.select_related('brand', 'category', 'line').prefetch_related(
            'images', 'tags',
        )

    def tagged(self, slug: str):
        return self.on_storefront().filter(tags__slug=slug).distinct()


class Product(TimeStampedModel):
    class Strength(models.TextChoices):
        MILD = 'mild', _('Легка')
        MEDIUM = 'medium', _('Середня')
        MEDIUM_FULL = 'medium_full', _('Середньо-повна')
        FULL = 'full', _('Повна')

    brand = models.ForeignKey(
        Brand, on_delete=models.PROTECT, related_name='products', verbose_name='Бренд',
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products', verbose_name='Категорія',
    )
    line = models.ForeignKey(
        ProductLine, null=True, blank=True, on_delete=models.SET_NULL, related_name='products',
        verbose_name='Лінія',
    )
    name = models.CharField('Назва', max_length=255)
    slug = models.SlugField(
        'Slug', max_length=280, unique=True, blank=True, help_text=_SLUG_HELP,
    )
    sku = models.CharField('SKU', max_length=64, blank=True, db_index=True)
    short_story = models.TextField('Коротка історія', blank=True)
    description = models.TextField('Опис', blank=True)
    tasting_notes = models.TextField('Смакові нотки', blank=True)
    recommendations = models.TextField('Рекомендації', blank=True)
    wrapper = models.CharField('Обгортка (wrapper)', max_length=120, blank=True)
    binder = models.CharField('Звʼязка (binder)', max_length=120, blank=True)
    filler = models.CharField('Начинка (filler)', max_length=120, blank=True)
    country = models.CharField('Країна виробника', max_length=80, blank=True)
    strength = models.CharField(
        'Міцність', max_length=32, choices=Strength.choices, blank=True,
    )
    smoke_time = models.CharField('Час куріння', max_length=64, blank=True)
    base_price = models.DecimalField(
        'Базова ціна', max_digits=10, decimal_places=2, default=Decimal('0'),
    )
    old_price = models.DecimalField(
        'Стара ціна', max_digits=10, decimal_places=2, null=True, blank=True,
    )
    currency = models.CharField('Валюта', max_length=3, default='UAH')
    stock = models.PositiveIntegerField(
        'Кількість на складі',
        default=0,
        help_text='Залишок на складі для цього SKU.',
    )
    is_active = models.BooleanField('Активний', default=True)
    is_featured = models.BooleanField('Рекомендований', default=False)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    video_url = models.URLField('URL відео', blank=True)
    video_file = models.FileField(
        'Відеофайл',
        upload_to='products/video/',
        blank=True,
        help_text='MP4/WebM. Має пріоритет над URL відео.',
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='products', verbose_name='Теги')
    meta_title = models.CharField('SEO-заголовок', max_length=255, blank=True)
    meta_description = models.TextField('SEO-опис', blank=True)
    views_count = models.PositiveIntegerField(default=0, editable=False)

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'category']),
            models.Index(fields=['is_active', 'brand']),
            models.Index(fields=['strength', 'country']),
        ]

    def __str__(self) -> str:
        return f'{self.brand.name} — {self.name}'

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            base = f'{self.brand.name}-{self.name}' if self.brand_id else self.name
            self.slug = unique_slug(self.__class__, base, max_length=280, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'slug': self.slug})

    @property
    def display_price(self) -> Decimal:
        return self.base_price

    def available_stock(self) -> int:
        return self.stock


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Файл фото', upload_to='products/')
    alt_text = models.CharField(
        'Підпис до фото',
        max_length=200,
        blank=True,
        help_text='Короткий опис зображення (для доступності та SEO).',
    )
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_primary = models.BooleanField('Головне фото', default=False)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото товару'

    def __str__(self) -> str:
        return self.alt_text or f'Фото #{self.pk}'


class ProductReview(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        'accounts.User', null=True, blank=True, on_delete=models.SET_NULL,
    )
    author_name = models.CharField('Імʼя', max_length=120)
    rating = models.PositiveSmallIntegerField('Оцінка', default=5)
    text = models.TextField('Відгук', blank=True)
    is_published = models.BooleanField('Опубліковано', default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
        constraints = [
            models.CheckConstraint(
                condition=Q(rating__gte=1) & Q(rating__lte=5),
                name='review_rating_1_5',
            ),
        ]
