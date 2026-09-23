"""Синхронізація оригінальних полів modeltranslation з *_uk у ModelForm."""

from __future__ import annotations

from django import forms
from django.conf import settings


def _translated_field_names(model) -> tuple[str, ...]:
    try:
        from modeltranslation.translator import translator
        opts = translator.get_options_for_model(model)
    except Exception:
        return ()
    if not opts or not opts.fields:
        return ()
    fields = opts.fields
    if isinstance(fields, dict):
        return tuple(fields.keys())
    return tuple(fields)


class TranslationSyncModelForm(forms.ModelForm):
    """
    Якщо оригінал (name) порожній, бере значення з name_uk (або default lang).
    Прибирає «тихі» помилки, коли JS ховає оригінальне поле.
    """

    def clean(self):
        cleaned = super().clean()
        default = getattr(settings, 'MODELTRANSLATION_DEFAULT_LANGUAGE', None) or 'uk'
        suffix = f'_{default.replace("-", "_")}'
        for base in _translated_field_names(self._meta.model):
            current = cleaned.get(base)
            if current not in (None, ''):
                continue
            lang_val = cleaned.get(f'{base}{suffix}')
            if lang_val not in (None, ''):
                cleaned[base] = lang_val
                self.cleaned_data[base] = lang_val
                # прибрати помилку «обов'язкове» з оригіналу
                if base in self._errors:
                    del self._errors[base]
        return cleaned
