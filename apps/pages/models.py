from django.db import models
from django.urls import reverse
from django.utils import timezone
from slugify import slugify


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


class BlogPost(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    slug = models.SlugField('Slug', max_length=280, unique=True)
    excerpt = models.TextField('Короткий опис', blank=True)
    body = models.TextField('Текст статті', blank=True)
    cover = models.ImageField(
        'Обкладинка', upload_to='blog/%Y/%m/', blank=True, null=True,
    )
    cover_alt = models.CharField('Alt обкладинки', max_length=255, blank=True)
    meta_title = models.CharField('SEO-заголовок', max_length=255, blank=True)
    meta_description = models.TextField('SEO-опис', blank=True)
    published_at = models.DateTimeField('Дата публікації', default=timezone.now)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)
    is_published = models.BooleanField('Опубліковано', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['-published_at', '-id']
        verbose_name = 'Стаття блогу'
        verbose_name_plural = 'Блог'
        indexes = [
            models.Index(fields=['is_published', '-published_at']),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:280]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('pages:blog_detail', kwargs={'slug': self.slug})

    @property
    def seo_title(self) -> str:
        return (self.meta_title or self.title).strip()

    @property
    def seo_description(self) -> str:
        text = (self.meta_description or self.excerpt or '').strip()
        return text[:160] if text else self.title


class BlogFAQItem(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='faq_items',
        verbose_name='Стаття',
    )
    question = models.CharField('Питання', max_length=255)
    answer = models.TextField('Відповідь')
    sort_order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['sort_order', 'id']
        verbose_name = 'FAQ статті'
        verbose_name_plural = 'FAQ статей'

    def __str__(self) -> str:
        return self.question
