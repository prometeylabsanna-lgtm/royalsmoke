from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_catalog_page_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroslide',
            name='cta_primary_label',
            field=models.CharField(
                blank=True, default='До каталогу', max_length=80,
                verbose_name='Текст основної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_primary_label_en',
            field=models.CharField(
                blank=True, default='До каталогу', max_length=80, null=True,
                verbose_name='Текст основної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_primary_label_uk',
            field=models.CharField(
                blank=True, default='До каталогу', max_length=80, null=True,
                verbose_name='Текст основної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_primary_label_zh_hans',
            field=models.CharField(
                blank=True, default='До каталогу', max_length=80, null=True,
                verbose_name='Текст основної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_primary_url',
            field=models.CharField(
                blank=True, default='/catalog/', max_length=255,
                verbose_name='Посилання основної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_secondary_label',
            field=models.CharField(
                blank=True, default='Сигари', max_length=80,
                verbose_name='Текст другорядної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_secondary_label_en',
            field=models.CharField(
                blank=True, default='Сигари', max_length=80, null=True,
                verbose_name='Текст другорядної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_secondary_label_uk',
            field=models.CharField(
                blank=True, default='Сигари', max_length=80, null=True,
                verbose_name='Текст другорядної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_secondary_label_zh_hans',
            field=models.CharField(
                blank=True, default='Сигари', max_length=80, null=True,
                verbose_name='Текст другорядної кнопки',
            ),
        ),
        migrations.AlterField(
            model_name='heroslide',
            name='cta_secondary_url',
            field=models.CharField(
                blank=True, default='/catalog/cigars/', max_length=255,
                verbose_name='Посилання другорядної кнопки',
            ),
        ),
    ]
