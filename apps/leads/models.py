from django.db import models


class Lead(models.Model):
    class Kind(models.TextChoices):
        CALLBACK = 'callback', 'Зворотний дзвінок'
        B2B = 'b2b', 'B2B запит'
        CHAT = 'chat', 'Чат'
        NEWSLETTER = 'newsletter', 'Підписка'
        CONTACT = 'contact', 'Контактна форма'

    kind = models.CharField('Тип', max_length=32, choices=Kind.choices)
    name = models.CharField('Імʼя', max_length=120, blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    company = models.CharField('Компанія', max_length=160, blank=True)
    message = models.TextField('Повідомлення', blank=True)
    payload = models.JSONField('Додаткові дані', default=dict, blank=True)
    source_url = models.CharField('Джерело', max_length=255, blank=True)
    is_processed = models.BooleanField('Оброблено', default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Лід'
        verbose_name_plural = 'Ліди'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.get_kind_display()} · {self.name or self.phone or self.email}'
