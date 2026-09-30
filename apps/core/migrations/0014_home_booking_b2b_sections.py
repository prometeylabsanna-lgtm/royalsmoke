from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_delivery_body_tinymce'),
    ]

    operations = [
        migrations.DeleteModel(name='HomeServiceSettings'),
        migrations.DeleteModel(name='B2bPageSettings'),
        migrations.DeleteModel(name='BookingPageSettings'),
        migrations.CreateModel(
            name='HomeBookingSettings',
            fields=[],
            options={
                'verbose_name': 'Бронювання',
                'verbose_name_plural': 'Бронювання',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
        migrations.CreateModel(
            name='HomeB2bSettings',
            fields=[],
            options={
                'verbose_name': 'B2B',
                'verbose_name_plural': 'B2B',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.sitesettings',),
        ),
    ]
