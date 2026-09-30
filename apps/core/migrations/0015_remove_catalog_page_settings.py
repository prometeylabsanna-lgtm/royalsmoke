from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_home_booking_b2b_sections'),
    ]

    operations = [
        migrations.DeleteModel(name='CatalogPageSettings'),
    ]
