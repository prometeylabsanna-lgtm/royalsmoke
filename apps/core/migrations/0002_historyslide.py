from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorySlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_label', models.CharField(max_length=40, verbose_name='Рік / мітка')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, verbose_name='Текст')),
                ('cta_label', models.CharField(blank=True, default='Читати далі', max_length=80, verbose_name='Текст кнопки')),
                ('cta_url', models.CharField(blank=True, default='/about/', max_length=255, verbose_name='URL кнопки')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Порядок')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активний')),
            ],
            options={
                'verbose_name': 'Слайд історії',
                'verbose_name_plural': 'Слайди історії',
                'ordering': ['sort_order', 'id'],
            },
        ),
    ]
