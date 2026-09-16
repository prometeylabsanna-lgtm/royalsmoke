from __future__ import annotations

from apps.core.models import SiteSettings


class HomeHeroSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Головний банер'
        verbose_name_plural = 'Головний банер'


class HomeBrandsSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Бренди'
        verbose_name_plural = 'Бренди'


class HomeCatalogSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Каталог на головній'
        verbose_name_plural = 'Каталог на головній'


class HomeAboutSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Історія сигар'
        verbose_name_plural = 'Історія сигар'


class HomeCalculatorSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Калькулятор'
        verbose_name_plural = 'Калькулятор'


class HomeServiceSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Сервіс'
        verbose_name_plural = 'Сервіс'


class AboutPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Про нас'
        verbose_name_plural = 'Про нас'


class FaqPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'FAQ — шапка'
        verbose_name_plural = 'FAQ — шапка'


class ContactPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Контакти'
        verbose_name_plural = 'Контакти'


class DeliveryPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'


class B2bPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'B2B'
        verbose_name_plural = 'B2B'


class BookingPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'


class CatalogPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Каталог — тексти'
        verbose_name_plural = 'Каталог — тексти'


class CartPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошик'


class CheckoutPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Оформлення'
        verbose_name_plural = 'Оформлення'


class CabinetPageSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Кабінет'
        verbose_name_plural = 'Кабінет'


class AgeGateSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Вікова перевірка'
        verbose_name_plural = 'Вікова перевірка'


class SiteHeaderSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Шапка'
        verbose_name_plural = 'Шапка'


class SiteFooterSettings(SiteSettings):
    class Meta:
        proxy = True
        verbose_name = 'Футер'
        verbose_name_plural = 'Футер'
