from __future__ import annotations

from django import forms

from apps.core.admin_site_content_widgets import (
    CmsAdminImageWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from apps.core.cms_i18n import CMS_LANGUAGES
from apps.core.models import HeroSlide, HistorySlide, HomeBrandCard
from apps.core.validation.admin_forms import clean_optional_url


class SkipEmptyBaseFormSet(forms.BaseModelFormSet):
    required_any: tuple[str, ...] = ()

    def save(self, commit=True):
        for form in self.extra_forms:
            data = getattr(form, 'cleaned_data', None)
            if not data or form.instance.pk:
                continue
            if not any(data.get(name) for name in self.required_any):
                data['DELETE'] = True
        return super().save(commit)


class HeroSlideBaseFormSet(SkipEmptyBaseFormSet):
    required_any = ('image', 'title_uk')


class HistorySlideBaseFormSet(SkipEmptyBaseFormSet):
    required_any = ('image', 'title_uk', 'year_label_uk')


class HomeBrandCardBaseFormSet(SkipEmptyBaseFormSet):
    required_any = ('brand', 'image')


def _i18n_widgets(*names: str) -> dict:
    widgets = {}
    for name in names:
        for _code, attr, _label in CMS_LANGUAGES:
            field = f'{name}_{attr}'
            if name in {'text', 'subtitle'}:
                widgets[field] = CmsAdminTextareaWidget(
                    attrs={'rows': 4 if name == 'text' else 2, 'data-cms-lang': _code},
                )
            else:
                widgets[field] = CmsAdminTextInputWidget(attrs={'data-cms-lang': _code})
    return widgets


def _i18n_fields(*names: str) -> tuple[str, ...]:
    fields = []
    for name in names:
        for _code, attr, _label in CMS_LANGUAGES:
            fields.append(f'{name}_{attr}')
    return tuple(fields)


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = (
            'image',
            *_i18n_fields('title', 'subtitle', 'cta_primary_label', 'cta_secondary_label'),
            'cta_primary_url',
            'cta_secondary_url',
            'sort_order',
            'is_active',
        )
        widgets = {
            **_i18n_widgets('title', 'subtitle', 'cta_primary_label', 'cta_secondary_label'),
            'image': CmsAdminImageWidget(),
            'cta_primary_url': CmsAdminTextInputWidget(),
            'cta_secondary_url': CmsAdminTextInputWidget(),
        }

    def clean_cta_primary_url(self):
        return clean_optional_url(self.cleaned_data.get('cta_primary_url', ''))

    def clean_cta_secondary_url(self):
        return clean_optional_url(self.cleaned_data.get('cta_secondary_url', ''))


HeroSlideFormSet = forms.modelformset_factory(
    HeroSlide, form=HeroSlideForm, formset=HeroSlideBaseFormSet, extra=1, can_delete=True,
)


class HistorySlideForm(forms.ModelForm):
    class Meta:
        model = HistorySlide
        fields = (
            *_i18n_fields('year_label', 'title', 'text', 'cta_label'),
            'image',
            'cta_url',
            'sort_order',
            'is_active',
        )
        widgets = {
            **_i18n_widgets('year_label', 'title', 'text', 'cta_label'),
            'image': CmsAdminImageWidget(),
            'cta_url': CmsAdminTextInputWidget(),
        }

    def clean_cta_url(self):
        return clean_optional_url(self.cleaned_data.get('cta_url', ''))


HistorySlideFormSet = forms.modelformset_factory(
    HistorySlide, form=HistorySlideForm, formset=HistorySlideBaseFormSet, extra=1, can_delete=True,
)


class HomeBrandCardForm(forms.ModelForm):
    class Meta:
        model = HomeBrandCard
        fields = (
            'brand',
            'image',
            *_i18n_fields('text'),
            'sort_order',
            'is_active',
        )
        widgets = {
            **_i18n_widgets('text'),
            'image': CmsAdminImageWidget(),
        }


HomeBrandCardFormSet = forms.modelformset_factory(
    HomeBrandCard, form=HomeBrandCardForm, formset=HomeBrandCardBaseFormSet, extra=1, can_delete=True,
)
