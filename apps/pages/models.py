from django.db import models


class FAQItem(models.Model):
    question = models.CharField('Питання', max_length=255)
    answer = models.TextField('Відповідь')
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активне', default=True)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'Питання FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self) -> str:
        return self.question


class LegalDocument(models.Model):
    slug = models.SlugField('Slug', max_length=64, unique=True)
    title = models.CharField('Заголовок', max_length=255)
    body = models.TextField('Текст', blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['sort_order', 'slug']
        verbose_name = 'Legal-документ'
        verbose_name_plural = 'Legal-документи'

    def __str__(self) -> str:
        return self.title
