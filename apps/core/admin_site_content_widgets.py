from __future__ import annotations

from typing import Any, Optional

from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget
from django.forms.widgets import ClearableFileInput
from tinymce.widgets import TinyMCE
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

    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        *,
        fallback_preview_url: str = '',
        preview_variant: str = 'photo',
    ) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        merged.setdefault('accept', 'image/*')
        classes = cms_control_classes(
            [c for c in INPUT_CLASSES if c != 'max-w-2xl'] + ['rs-cms-image-input'],
            extra_class,
        )
        self.fallback_preview_url = (fallback_preview_url or '').strip()
        self.preview_variant = preview_variant if preview_variant in {'photo', 'icon'} else 'photo'
        super().__init__(attrs={**merged, 'class': classes})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        preview_url = ''
        if value:
            try:
                preview_url = getattr(value, 'url', '') or ''
            except ValueError:
                preview_url = ''
        is_fallback = False
        if not preview_url and self.fallback_preview_url:
            preview_url = self.fallback_preview_url
            is_fallback = True
        context['widget']['preview_url'] = preview_url
        context['widget']['preview_is_fallback'] = is_fallback
        context['widget']['preview_variant'] = self.preview_variant
        return context


class CmsAdminFileWidget(ClearableFileInput):
    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        merged.setdefault('accept', 'video/mp4,video/webm,video/ogg,.mp4,.webm,.ogg')
        classes = cms_control_classes(INPUT_CLASSES, extra_class)
        super().__init__(attrs={**merged, 'class': classes})


class CmsAdminColorWidget(AdminTextInputWidget):
    input_type = 'color'
    template_name = 'django/forms/widgets/cms_color.html'

    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        *,
        default_color: str = '#100d0c',
    ) -> None:
        self.default_color = self._normalize_hex(default_color) or '#100d0c'
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        super().__init__(attrs={
            **merged,
            'class': cms_control_classes(['rs-cms-colorpick__native'], extra_class),
        })

    @staticmethod
    def _normalize_hex(value: str) -> str:
        raw = (value or '').strip()
        if not raw:
            return ''
        if len(raw) == 4 and raw.startswith('#'):
            return f'#{raw[1] * 2}{raw[2] * 2}{raw[3] * 2}'.lower()
        return raw.lower()

    def format_value(self, value):
        raw = self._normalize_hex(value or '')
        return raw or self.default_color

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['default_color'] = self.default_color
        return context


class CmsAdminTinyMCEWidget(TinyMCE):
    def __init__(
        self,
        attrs: Optional[dict[str, Any]] = None,
        mce_attrs: Optional[dict[str, Any]] = None,
    ) -> None:
        merged = dict(attrs or {})
        extra_class = merged.pop('class', '')
        mce = {
            'height': 280,
            'menubar': False,
            'plugins': 'link lists code',
            'toolbar': 'undo redo | bold italic underline | bullist numlist | link | code',
            'branding': False,
            'promotion': False,
            **(mce_attrs or {}),
        }
        super().__init__(
            attrs={
                **merged,
                'class': cms_control_classes(TEXTAREA_CLASSES, extra_class),
            },
            mce_attrs=mce,
        )
