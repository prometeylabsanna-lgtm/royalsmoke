from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_product_stock_label'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productvariant',
            options={
                'ordering': ['sort_order', 'price'],
                'verbose_name': 'Формат сигари',
                'verbose_name_plural': 'Формати сигари (розміри)',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(
                default=0,
                help_text=(
                    'Для товарів без форматів. Якщо є формати сигари нижче — '
                    'вказуйте кількість у кожному форматі.'
                ),
                verbose_name='Кількість на складі',
            ),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='name',
            field=models.CharField(
                help_text='Наприклад: Robusto, Churchill. У сигар це називають вітолою.',
                max_length=120,
                verbose_name='Назва формату',
            ),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='ring_gauge',
            field=models.PositiveIntegerField(
                blank=True,
                help_text='Діаметр сигари в 64-х частках дюйма.',
                null=True,
                verbose_name='Товщина (ring gauge)',
            ),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='sku',
            field=models.CharField(blank=True, max_length=64, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='stock',
            field=models.PositiveIntegerField(default=0, verbose_name='Кількість на складі'),
        ),
    ]
