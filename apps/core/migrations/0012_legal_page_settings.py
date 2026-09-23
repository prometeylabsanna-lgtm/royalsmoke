from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_chromestyle'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivacyPageSettings',
            fields=[],
            options={
                'verbose_name': 'Політика конфіденційності',
                'verbose_name_plural': 'Політика конфіденційності',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
        migrations.CreateModel(
            name='TermsPageSettings',
            fields=[],
            options={
                'verbose_name': 'Умови користування',
                'verbose_name_plural': 'Умови користування',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
        migrations.CreateModel(
            name='AgePolicyPageSettings',
            fields=[],
            options={
                'verbose_name': 'Вікова політика',
                'verbose_name_plural': 'Вікова політика',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
        migrations.CreateModel(
            name='CookiesPageSettings',
            fields=[],
            options={
                'verbose_name': 'Файли cookie',
                'verbose_name_plural': 'Файли cookie',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
    ]
