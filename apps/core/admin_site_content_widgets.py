from __future__ import annotations

from typing import Any, Optional

from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from django.forms.widgets import ClearableFileInput
from unfold.widgets import INPUT_CLASSES, TEXTAREA_CLASSES


def cms_control_classes(base_classes: list[str], extra_class: str = '') -> str:
    """Keep Unfold theme-aware classes (light + dark:), only append extras."""
    classes = list(base_classes)
    if extra_class:
        for token in extra_class.split():
            if token and token not in classes:
                classes.append(token)
    return ' '.join(classes)


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        super().__init__(attrs={
            **merged,
            'class': cms_control_classes(INPUT_CLASSES, extra_class),
        })


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        super().__init__(attrs={
            **merged,
            'class': cms_control_classes(TEXTAREA_CLASSES, extra_class),
        })


class CmsAdminImageWidget(ClearableFileInput):
    template_name = 'django/forms/widgets/cms_image.html'

    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        merged.setdefault('accept', 'image/*')
        classes = cms_control_classes(
            [c for c in INPUT_CLASSES if c != 'max-w-2xl'] + ['rs-cms-image-input'],
            extra_class,
        )
        super().__init__(attrs={**merged, 'class': classes})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        preview_url = ''
        if value:
            try:
                preview_url = getattr(value, 'url', '') or ''
            except ValueError:
                preview_url = ''
        context['widget']['preview_url'] = preview_url
        return context
