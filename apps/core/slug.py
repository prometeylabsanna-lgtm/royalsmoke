"""Унікальний slug з назви (кирилиця → латиниця через python-slugify)."""

from __future__ import annotations

from slugify import slugify


def unique_slug(
    model_cls,
    source: str,
    *,
    max_length: int = 200,
    instance=None,
    slug_field: str = 'slug',
    extra_filter: dict | None = None,
) -> str:
    base = (slugify(source or '') or 'item')[:max_length]
    candidate = base
    n = 2
    while True:
        qs = model_cls.objects.filter(**{slug_field: candidate})
        if extra_filter:
            qs = qs.filter(**extra_filter)
        if instance is not None and getattr(instance, 'pk', None):
            qs = qs.exclude(pk=instance.pk)
        if not qs.exists():
            return candidate
        suffix = f'-{n}'
        candidate = f'{base[: max_length - len(suffix)]}{suffix}'
        n += 1
