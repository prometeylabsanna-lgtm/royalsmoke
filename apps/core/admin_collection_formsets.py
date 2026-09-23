from __future__ import annotations

from django import forms

from apps.core.admin_site_content_widgets import (
    CmsAdminImageWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from apps.core.cms_i18n import CMS_LANGUAGES
from apps.core.cms_text_normalize import sanitize_cms_storage
from apps.core.models import DeliveryCard, HeroSlide, HistorySlide, HomeBrandCard
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


class DeliveryCardBaseFormSet(SkipEmptyBaseFormSet):
    required_any = ('title_uk',)
    card_kind: str = DeliveryCard.Kind.REGION

    def save(self, commit=True):
        for form in self.extra_forms:
            data = getattr(form, 'cleaned_data', None)
            if not data or form.instance.pk:
                continue
            if not any(data.get(name) for name in self.required_any):
                data['DELETE'] = True
        instances = forms.BaseModelFormSet.save(self, commit=False)
        for obj in instances:
            obj.kind = self.card_kind
            if commit:
                obj.save()
        if commit:
            self.save_m2m()
            for obj in self.deleted_objects:
                obj.delete()
        return instances


class DeliveryRegionFormSetBase(DeliveryCardBaseFormSet):
    card_kind = DeliveryCard.Kind.REGION


class DeliveryPaymentFormSetBase(DeliveryCardBaseFormSet):
    card_kind = DeliveryCard.Kind.PAYMENT


def _i18n_widgets(*names: str) -> dict:
    widgets = {}
    for name in names:
        for _code, attr, _label in CMS_LANGUAGES:
            field = f'{name}_{attr}'
            if name in {'text', 'subtitle'}:
                widgets[field] = CmsAdminTextareaWidget(
                    attrs={'rows': 3 if name == 'text' else 2, 'data-cms-lang': _code},
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


def _sanitize_text_fields(form: forms.ModelForm, *names: str) -> None:
    for name in names:
        for _code, attr, _label in CMS_LANGUAGES:
            field = f'{name}_{attr}'
            if field in form.cleaned_data:
                form.cleaned_data[field] = sanitize_cms_storage(name, form.cleaned_data.get(field))


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

    def clean(self):
        cleaned = super().clean()
        _sanitize_text_fields(self, 'title', 'subtitle', 'cta_primary_label', 'cta_secondary_label')
        return cleaned

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

    def clean(self):
        cleaned = super().clean()
        _sanitize_text_fields(self, 'year_label', 'title', 'text', 'cta_label')
        return cleaned

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

    def clean(self):
        cleaned = super().clean()
        _sanitize_text_fields(self, 'text')
        return cleaned


HomeBrandCardFormSet = forms.modelformset_factory(
    HomeBrandCard, form=HomeBrandCardForm, formset=HomeBrandCardBaseFormSet, extra=1, can_delete=True,
)


class DeliveryCardForm(forms.ModelForm):
    class Meta:
        model = DeliveryCard
        fields = (
            *_i18n_fields('title', 'text'),
            'sort_order',
            'is_active',
        )
        widgets = {
            **_i18n_widgets('title', 'text'),
        }

    def clean(self):
        cleaned = super().clean()
        _sanitize_text_fields(self, 'title', 'text')
        return cleaned


DeliveryRegionFormSet = forms.modelformset_factory(
    DeliveryCard,
    form=DeliveryCardForm,
    formset=DeliveryRegionFormSetBase,
    extra=1,
    can_delete=True,
)

DeliveryPaymentFormSet = forms.modelformset_factory(
    DeliveryCard,
    form=DeliveryCardForm,
    formset=DeliveryPaymentFormSetBase,
    extra=1,
    can_delete=True,
)
