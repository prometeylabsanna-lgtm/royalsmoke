from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_fx_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='variant',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='variant_name',
        ),
    ]
