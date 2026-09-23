from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_remove_cigarettes_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={
                'ordering': ['sort_order', 'id'],
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото товару',
            },
        ),
        migrations.AlterField(
            model_name='productimage',
            name='alt_text',
            field=models.CharField(
                blank=True,
                help_text='Короткий опис зображення (для доступності та SEO).',
                max_length=200,
                verbose_name='Підпис до фото',
            ),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products/', verbose_name='Файл фото'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='is_primary',
            field=models.BooleanField(default=False, verbose_name='Головне фото'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='sort_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
    ]
