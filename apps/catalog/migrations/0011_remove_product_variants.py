from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_remove_product_variants'),
        ('catalog', '0010_productimage_ua_labels'),
        ('orders', '0004_remove_product_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Залишок на складі для цього SKU.',
                verbose_name='Кількість на складі',
            ),
        ),
        migrations.DeleteModel(
            name='ProductVariant',
        ),
    ]
