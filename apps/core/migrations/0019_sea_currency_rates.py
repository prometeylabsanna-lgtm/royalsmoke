from decimal import Decimal

from django.db import migrations

# Орієнтовні курси; актуальні значення редактор виставляє в адмінці «Курси валют».
RATES = (
    ('MYR', 'Малайзійський рингіт', 'RM', Decimal('9.76000000'), 3),
    ('PHP', 'Філіппінське песо', '₱', Decimal('0.70000000'), 4),
    ('IDR', 'Індонезійська рупія', 'Rp', Decimal('0.00250000'), 5),
    ('VND', 'В’єтнамський донг', '₫', Decimal('0.00156000'), 6),
)


def seed_rates(apps, schema_editor):
    CurrencyRate = apps.get_model('core', 'CurrencyRate')
    for code, name, symbol, rate, order in RATES:
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
    CurrencyRate.objects.filter(code__in=[row[0] for row in RATES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_currency_rate_precision'),
    ]

    operations = [
        migrations.RunPython(seed_rates, unseed_rates),
    ]
