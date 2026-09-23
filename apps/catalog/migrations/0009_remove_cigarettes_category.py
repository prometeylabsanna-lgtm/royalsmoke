from django.db import migrations, models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


def remove_cigarettes(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    Product = apps.get_model('catalog', 'Product')
    qs = Category.objects.filter(
        Q(kind='cigarettes') | Q(slug='cigarettes') | Q(name='Сигарети')
    )
    # Перенести товари в «Сигари» або «Інше», якщо такі є
    cigars = Category.objects.filter(slug='cigars').first()
    for cat in qs:
        products = Product.objects.filter(category_id=cat.pk)
        if cigars is not None:
            products.update(category_id=cigars.pk)
        else:
            products.delete()
        cat.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_slug_blank_auto'),
    ]

    operations = [
        migrations.RunPython(remove_cigarettes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='kind',
            field=models.CharField(
                choices=[
                    ('cigars', 'Сигари'),
                    ('accessories', 'Аксесуари'),
                    ('other', 'Інше'),
                ],
                default='cigars',
                max_length=32,
                verbose_name='Тип',
            ),
        ),
    ]
