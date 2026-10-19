from django.db import migrations


def _schema_matches_models(connection, models) -> bool:
    """True, якщо в БД уже є всі колонки живих моделей.

    Цей крок працює з живими моделями, а не з історичними. На чистій БД пізніші
    міграції (наприклад колонки нових мов modeltranslation) ще не застосовані, тож
    запит до моделі впав би. Тоді крок пропускаємо: ті самі ensure_* викликає
    seed_demo одразу після migrate (deploy/entrypoint.sh).
    """
    tables = set(connection.introspection.table_names())
    with connection.cursor() as cursor:
        for model in models:
            table = model._meta.db_table
            if table not in tables:
                return False
            columns = {col.name for col in connection.introspection.get_table_description(cursor, table)}
            if not {field.column for field in model._meta.concrete_fields} <= columns:
                return False
    return True


def forwards(apps, schema_editor):
    from apps.core.delivery_cards import ensure_delivery_cards
    from apps.core.legal_delivery_migrate import (
        ensure_delivery_body_block,
        ensure_delivery_header_blocks,
    )
    from apps.core.models import DeliveryCard, SiteBlock

    if not _schema_matches_models(schema_editor.connection, (SiteBlock, DeliveryCard)):
        return

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
