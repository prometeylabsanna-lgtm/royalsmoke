from django.db import migrations


def forwards(apps, schema_editor):
    from apps.core.delivery_cards import ensure_delivery_cards
    from apps.core.legal_delivery_migrate import (
        ensure_delivery_body_block,
        ensure_delivery_header_blocks,
    )

    ensure_delivery_cards()
    ensure_delivery_header_blocks()
    ensure_delivery_body_block(force=False)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_legal_page_settings'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
