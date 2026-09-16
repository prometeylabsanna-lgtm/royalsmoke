from __future__ import annotations

from django.db import models
from django.utils.html import format_html

from apps.core.admin_site_content_widgets import CmsAdminImageWidget


def image_thumb(filefield, alt: str = '') -> str:
    try:
        url = filefield.url
    except (ValueError, AttributeError):
        return '—'
    if not url:
        return '—'
    return format_html('<img src="{}" class="rs-admin-thumb" alt="{}">', url, alt)


class ImagePreviewAdminMixin:
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.ImageField):
            kwargs['widget'] = CmsAdminImageWidget()
        return super().formfield_for_dbfield(db_field, request, **kwargs)
