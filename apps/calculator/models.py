from django.db import models
from django.utils.translation import gettext_lazy as _


class CalculatorQuestion(models.Model):
    """Крок опитування калькулятора підбору."""

    STEP_STRENGTH = 'strength'
    STEP_FORMAT = 'format'
    STEP_COUNTRY = 'country'
    STEP_BUDGET = 'budget'
    STEP_CHOICES = [
        (STEP_STRENGTH, _('Міцність')),
        (STEP_FORMAT, _('Формат')),
        (STEP_COUNTRY, _('Країна')),
        (STEP_BUDGET, _('Бюджет')),
    ]

    step_key = models.CharField('Крок', max_length=32, choices=STEP_CHOICES, unique=True)
    title = models.CharField('Заголовок', max_length=200)
    help_text = models.CharField('Підказка', max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Крок калькулятора'
        verbose_name_plural = 'Кроки калькулятора'
        ordering = ['sort_order']

    def __str__(self) -> str:
        return self.title


class CalculatorOption(models.Model):
    question = models.ForeignKey(
        CalculatorQuestion, on_delete=models.CASCADE, related_name='options',
    )
    label = models.CharField('Варіант', max_length=120)
    value = models.CharField('Значення', max_length=64)
    filter_field = models.CharField(
        'Поле фільтра',
        max_length=64,
        help_text='напр. strength / country / shape / budget_max',
    )
    filter_value = models.CharField('Значення фільтра', max_length=64)
    explanation = models.CharField('Пояснення', max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Варіант відповіді'
        verbose_name_plural = 'Варіанти відповідей'
        ordering = ['sort_order', 'id']

    def __str__(self) -> str:
        return f'{self.question.step_key}: {self.label}'
