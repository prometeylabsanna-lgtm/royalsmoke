from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.slug import unique_slug

_SLUG_HELP = 'Заповнюється автоматично з назви. Можна залишити порожнім.'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    class Kind(models.TextChoices):
        CIGARS = 'cigars', _('Сигари')
        CIGARETTES = 'cigarettes', _('Сигарети')
        ACCESSORIES = 'accessories', _('Аксесуари')
        OTHER = 'other', _('Інше')

    name = models.CharField('Назва', max_length=200)
    slug = models.SlugField(
        'Slug', max_length=220, unique=True, blank=True, help_text=_SLUG_HELP,
    )
    kind = models.CharField('Тип', max_length=32, choices=Kind.choices, default=Kind.CIGARS)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE,
        related_name='children', verbose_name='Батьківська',
    )
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='categories/', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)
    is_featured = models.BooleanField('На головній', default=False)
    meta_title = models.CharField('SEO-заголовок', max_length=255, blank=True)
    meta_description = models.TextField('SEO-опис', blank=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            self.slug = unique_slug(self.__class__, self.name, max_length=220, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category', kwargs={'slug': self.slug})


class Brand(TimeStampedModel):
    name = models.CharField('Назва', max_length=160)
    slug = models.SlugField(
        'Slug', max_length=180, unique=True, blank=True, help_text=_SLUG_HELP,
    )
    country = models.CharField('Країна', max_length=80, blank=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True)
    short_description = models.TextField('Короткий опис', blank=True)
    description = models.TextField('Опис', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)
    is_featured = models.BooleanField('На головній', default=False)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            self.slug = unique_slug(self.__class__, self.name, max_length=180, instance=self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:brand', kwargs={'slug': self.slug})


class ProductLine(TimeStampedModel):
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='lines', verbose_name='Бренд',
    )
    name = models.CharField('Назва лінії', max_length=160)
    slug = models.SlugField(
        'Slug', max_length=180, unique=True, blank=True, help_text=_SLUG_HELP,
    )
    description = models.TextField('Опис', blank=True)
    image = models.ImageField('Зображення', upload_to='lines/', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Лінія'
        verbose_name_plural = 'Лінії'
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return f'{self.brand.name} · {self.name}'

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            base = f'{self.brand.name}-{self.name}' if self.brand_id else self.name
            self.slug = unique_slug(self.__class__, base, max_length=180, instance=self)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Теги рекомендацій: top, new, related — без ШІ."""

    slug = models.SlugField(
        'Slug', unique=True, max_length=64, blank=True, help_text=_SLUG_HELP,
    )
    name = models.CharField('Назва', max_length=80)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            self.slug = unique_slug(self.__class__, self.name, max_length=64, instance=self)
        super().save(*args, **kwargs)
