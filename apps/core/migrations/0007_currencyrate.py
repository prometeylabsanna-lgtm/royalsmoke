from decimal import Decimal

from django.db import migrations, models


def seed_rates(apps, schema_editor):
    CurrencyRate = apps.get_model('core', 'CurrencyRate')
    rows = (
        ('UAH', 'Гривня', '₴', Decimal('1'), 0),
        ('USD', 'Долар США', '$', Decimal('41.0000'), 1),
        ('CNY', 'Юань', '¥', Decimal('5.8000'), 2),
    )
    for code, name, symbol, rate, order in rows:
        CurrencyRate.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'symbol': symbol,
                'uah_per_unit': rate,
                'sort_order': order,
            },
        )


def unseed_rates(apps, schema_editor):
    CurrencyRate = apps.get_model('core', 'CurrencyRate')
    CurrencyRate.objects.filter(code__in=('UAH', 'USD', 'CNY')).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_blog_page_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'code',
                    models.CharField(
                        help_text='USD, CNY, EUR… Для нової мови додайте валюту тут і рядок у LANGUAGE_CURRENCY.',
                        max_length=3,
                        unique=True,
                        verbose_name='Код ISO',
                    ),
                ),
                ('name', models.CharField(max_length=64, verbose_name='Назва')),
                ('symbol', models.CharField(max_length=8, verbose_name='Символ')),
                (
                    'uah_per_unit',
                    models.DecimalField(
                        decimal_places=4,
                        help_text='Скільки гривень коштує 1 одиниця цієї валюти. Для UAH завжди 1.',
                        max_digits=12,
                        verbose_name='Гривень за 1 одиницю',
                    ),
                ),
                (
                    'sort_order',
                    models.PositiveSmallIntegerField(default=0, verbose_name='Порядок'),
                ),
            ],
            options={
                'verbose_name': 'Курс валюти',
                'verbose_name_plural': 'Курси валют',
                'ordering': ['sort_order', 'code'],
            },
        ),
        migrations.RunPython(seed_rates, unseed_rates),
    ]
