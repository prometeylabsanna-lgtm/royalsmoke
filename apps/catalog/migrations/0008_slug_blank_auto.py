from django.db import migrations, models


_HELP = 'Заповнюється автоматично з назви. Можна залишити порожнім.'


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_variant_friendly_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=220, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=180, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='productline',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=180, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=64, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=280, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='slug',
            field=models.SlugField(blank=True, help_text=_HELP, max_length=140, verbose_name='Slug'),
        ),
    ]
