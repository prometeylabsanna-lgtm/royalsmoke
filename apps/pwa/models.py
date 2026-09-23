from __future__ import annotations

from django.conf import settings
from django.db import models


class PushSubscription(models.Model):
    """Browser Web Push endpoint; user and/or email for order targeting."""

    endpoint = models.URLField(max_length=500, unique=True)
    p256dh = models.CharField(max_length=200)
    auth = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='push_subscriptions',
    )
    email = models.EmailField(blank=True, db_index=True)
    language = models.CharField(max_length=16, default='uk')
    user_agent = models.CharField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Push-підписка'
        verbose_name_plural = 'Push-підписки'
        ordering = ['-updated_at']

    def __str__(self) -> str:
        who = self.email or (self.user_id and f'user:{self.user_id}') or 'guest'
        return f'{who} · {self.endpoint[:48]}'
