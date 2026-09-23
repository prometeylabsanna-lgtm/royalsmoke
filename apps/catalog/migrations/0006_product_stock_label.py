from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_cms_page_style_video_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(
                default=0,
                help_text='Для товарів без форматів. Якщо є формати сигари нижче — вказуйте кількість у кожному форматі.',
                verbose_name='Кількість на складі',
            ),
        ),
    ]
