from __future__ import annotations

from django.db import models

from apps.core.slug import unique_slug

_SLUG_HELP = 'Заповнюється автоматично. Можна залишити порожнім.'


class MobileSettings(models.Model):
    """Singleton налаштувань застосунку (pk=1)."""

    app_version = models.CharField('Версія в UI', max_length=64, default='Royal Smoke · v1.0')
    app_blurb = models.TextField('Короткий опис', blank=True)
    contact_address = models.CharField('Адреса', max_length=255, blank=True)
    contact_phone = models.CharField('Телефон', max_length=64, blank=True)
    contact_hours = models.CharField('Години роботи', max_length=255, blank=True)
    contact_lat = models.FloatField('Широта', default=50.4501)
    contact_lng = models.FloatField('Довгота', default=30.5226)
    app_seal = models.ImageField(
        'Печатка в застосунку',
        upload_to='mobile/seal/',
        blank=True,
        help_text='Іконка/печатка всередині апки (splash, Ще). Не змінює App Icon у Store.',
    )
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Налаштування застосунку'
        verbose_name_plural = 'Налаштування застосунку'

    def __str__(self) -> str:
        return 'Налаштування мобільного застосунку'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return None

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class MobileBrand(models.Model):
    class Panel(models.TextChoices):
        AMBER = 'amber', 'Amber'
        BURGUNDY = 'burgundy', 'Burgundy'
        GREEN = 'green', 'Green'
        BROWN = 'brown', 'Brown'

    slug = models.SlugField('Slug', max_length=64, unique=True, blank=True, help_text=_SLUG_HELP)
    name = models.CharField('Назва', max_length=160)
    short_name = models.CharField('Коротка назва', max_length=80, blank=True)
    mono = models.CharField('Монограма', max_length=8, blank=True)
    country = models.CharField('Країна', max_length=80, blank=True)
    panel = models.CharField(
        'Колір панелі', max_length=16, choices=Panel.choices, default=Panel.AMBER,
    )
    cover = models.ImageField('Обкладинка', upload_to='mobile/brands/', blank=True)
    heritage = models.TextField('Історія / heritage', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Бренд гайду'
        verbose_name_plural = 'Бренди гайду'
        ordering = ['sort_order', 'name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not (self.slug or '').strip():
            self.slug = unique_slug(self.__class__, self.name, max_length=64, instance=self)
        if not self.short_name:
            self.short_name = self.name
        super().save(*args, **kwargs)


class MobileBrandFact(models.Model):
    brand = models.ForeignKey(
        MobileBrand, on_delete=models.CASCADE, related_name='facts', verbose_name='Бренд',
    )
    label = models.CharField('Мітка', max_length=120)
    value = models.CharField('Значення', max_length=255)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Факт бренду'
        verbose_name_plural = 'Факти бренду'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return f'{self.label}: {self.value}'


class MobileBrandLine(models.Model):
    brand = models.ForeignKey(
        MobileBrand, on_delete=models.CASCADE, related_name='lines', verbose_name='Бренд',
    )
    name = models.CharField('Назва лінії', max_length=160)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Лінія бренду'
        verbose_name_plural = 'Лінії бренду'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return self.name


class MobileBrandPhoto(models.Model):
    brand = models.ForeignKey(
        MobileBrand, on_delete=models.CASCADE, related_name='photos', verbose_name='Бренд',
    )
    image = models.ImageField('Фото', upload_to='mobile/brands/photos/')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        verbose_name = 'Фото бренду'
        verbose_name_plural = 'Фото брендів'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return f'Фото {self.brand_id} #{self.pk or "нове"}'


class MobileScreen(models.Model):
    class Key(models.TextChoices):
        SPLASH = 'splash', 'Splash'
        AGE = 'age', 'Вікова перевірка'
        HOME = 'home', 'Головна'
        HOUSE = 'house', 'Дім'
        VISIT = 'visit', 'Візит'

    key = models.CharField('Екран', max_length=32, choices=Key.choices, unique=True)
    kicker = models.CharField('Kicker', max_length=120, blank=True)
    title = models.CharField('Заголовок', max_length=255, blank=True)
    subtitle = models.CharField('Підзаголовок', max_length=255, blank=True)
    body = models.TextField('Текст', blank=True)
    body_secondary = models.TextField('Текст (дод.)', blank=True)
    cta_primary = models.CharField('CTA основна', max_length=120, blank=True)
    cta_secondary = models.CharField('CTA друга', max_length=120, blank=True)
    confirm_label = models.CharField('Кнопка підтвердження', max_length=120, blank=True)
    legal_note = models.TextField('Юридична примітка', blank=True)
    success_title = models.CharField('Успіх: заголовок', max_length=255, blank=True)
    success_body = models.TextField('Успіх: текст', blank=True)
    hero_image = models.ImageField('Hero / фото', upload_to='mobile/screens/', blank=True)
    is_active = models.BooleanField('Активний', default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Екран застосунку'
        verbose_name_plural = 'Екрани застосунку'
        ordering = ['key']

    def __str__(self) -> str:
        return self.get_key_display()


class MobileHouseBlock(models.Model):
    screen = models.ForeignKey(
        MobileScreen,
        on_delete=models.CASCADE,
        related_name='house_blocks',
        verbose_name='Екран',
        limit_choices_to={'key': MobileScreen.Key.HOUSE},
    )
    index_label = models.CharField('Індекс', max_length=8, default='01')
    title = models.CharField('Заголовок', max_length=120)
    body = models.TextField('Текст', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Блок «Дім»'
        verbose_name_plural = 'Блоки «Дім»'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return f'{self.index_label} {self.title}'


class MobileLegalPage(models.Model):
    class Slug(models.TextChoices):
        PRIVACY = 'privacy', 'Політика конфіденційності'
        TERMS = 'terms', 'Умови'
        AGE = 'age', 'Вікова політика'
        ABOUT = 'about', 'Про застосунок'

    slug = models.SlugField('Slug', max_length=32, unique=True, choices=Slug.choices)
    title = models.CharField('Заголовок', max_length=255)
    body = models.TextField('Текст')
    is_active = models.BooleanField('Активна', default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Юридична сторінка'
        verbose_name_plural = 'Юридичні сторінки'
        ordering = ['slug']

    def __str__(self) -> str:
        return self.title
