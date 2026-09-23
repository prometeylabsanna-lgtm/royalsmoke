from django.db import migrations, models


def seed_chrome(apps, schema_editor):
    ChromeStyle = apps.get_model('core', 'ChromeStyle')
    ChromeStyle.objects.get_or_create(pk=1)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_page_style_text_accent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChromeStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_bg', models.CharField(blank=True, max_length=32, verbose_name='Шапка — фон')),
                ('header_text', models.CharField(blank=True, max_length=32, verbose_name='Шапка — шрифт')),
                ('footer_top_bg', models.CharField(blank=True, max_length=32, verbose_name='Підвал (верх) — фон')),
                ('footer_top_text', models.CharField(blank=True, max_length=32, verbose_name='Підвал (верх) — шрифт')),
                ('footer_bottom_bg', models.CharField(blank=True, max_length=32, verbose_name='Підвал (низ) — фон')),
                ('footer_bottom_text', models.CharField(blank=True, max_length=32, verbose_name='Підвал (низ) — шрифт')),
            ],
            options={
                'verbose_name': 'Шапка і підвал',
                'verbose_name_plural': 'Шапка і підвал',
            },
        ),
        migrations.RunPython(seed_chrome, migrations.RunPython.noop),
    ]
