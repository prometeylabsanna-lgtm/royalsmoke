from __future__ import annotations

from django import forms
from django.contrib import messages
from django.core.cache import cache
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unfold.widgets import UnfoldAdminFileFieldWidget, UnfoldBooleanWidget

from apps.core.admin_site_content_widgets import CmsAdminTextInputWidget, CmsAdminTextareaWidget
from apps.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    INLINE_KEYS,
    MULTILINE_KEYS,
    is_visibility_key,
)
from apps.core.models import HeroSlide, HistorySlide, SiteBlock, SiteSettings
from apps.core.site_content_registry import (
    ContentSection,
    get_block_field_label,
    get_section,
    iter_section_blocks,
)

SECTION_VISIBLE_FIELD = 'section_visible'
SITE_BLOCKS_CACHE_KEY = 'site_blocks'


def block_field_name(page: str, key: str, suffix: str) -> str:
    return f'block__{page}__{key}__{suffix}'


def load_section_blocks(section: ContentSection) -> dict[tuple[str, str], SiteBlock]:
    blocks: dict[tuple[str, str], SiteBlock] = {}
    for page, key in iter_section_blocks(section):
        content_type = BLOCK_CONTENT_TYPES.get((page, key), SiteBlock.ContentType.TEXT)
        block, _ = SiteBlock.objects.get_or_create(
            page=page,
            key=key,
            defaults={
                'label': get_block_field_label(page, key),
                'content_type': content_type,
                'text_html': BLOCK_DEFAULTS.get(
                    (page, key), '1' if is_visibility_key(key) else '',
                ),
                'sort_order': 0,
                'is_active': True,
            },
        )
        blocks[(page, key)] = block
    return blocks


class SitePageContentForm(forms.Form):
    def __init__(self, section: ContentSection, blocks, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = section
        self.blocks = blocks

        if section.visibility_key:
            page, key = self._visibility_page_key(section)
            block = blocks[(page, key)]
            self.fields[SECTION_VISIBLE_FIELD] = forms.BooleanField(
                label='Показувати секцію на сайті',
                required=False,
                initial=block.text_html.strip() in {'1', 'true', 'True'},
                widget=UnfoldBooleanWidget(),
            )

        for page, key in section.blocks:
            self._add_block_fields(blocks[(page, key)])

    def _visibility_page_key(self, section: ContentSection) -> tuple[str, str]:
        for page, key in iter_section_blocks(section):
            if key == section.visibility_key:
                return page, key
        raise KeyError(section.visibility_key)

    def _add_block_fields(self, block: SiteBlock) -> None:
        page, key = block.page, block.key
        label = get_block_field_label(page, key)
        if is_visibility_key(key) and key != self.section.visibility_key:
            self.fields[block_field_name(page, key, 'visible')] = forms.BooleanField(
                label=label,
                required=False,
                initial=block.text_html.strip() in {'1', 'true', 'True'},
                widget=UnfoldBooleanWidget(),
            )
            return
        if block.content_type == SiteBlock.ContentType.IMAGE:
            self.fields[block_field_name(page, key, 'image')] = forms.ImageField(
                label=label,
                required=False,
                widget=UnfoldAdminFileFieldWidget(),
            )
            return
        widget = (
            CmsAdminTextInputWidget()
            if key in INLINE_KEYS
            else CmsAdminTextareaWidget(attrs={'rows': 4 if key in MULTILINE_KEYS else 2})
        )
        self.fields[block_field_name(page, key, 'text_html')] = forms.CharField(
            label=label, initial=block.text_html, required=False, widget=widget,
        )

    def save(self) -> None:
        if SECTION_VISIBLE_FIELD in self.fields:
            page, key = self._visibility_page_key(self.section)
            block = self.blocks[(page, key)]
            block.text_html = '1' if self.cleaned_data.get(SECTION_VISIBLE_FIELD) else '0'
            block.is_active = True
            block.save()

        for block in self.blocks.values():
            page, key = block.page, block.key
            if key == self.section.visibility_key:
                continue
            if is_visibility_key(key):
                block.text_html = '1' if self.cleaned_data.get(
                    block_field_name(page, key, 'visible'),
                ) else '0'
                block.is_active = True
                block.save()
                continue
            block.is_active = True
            if block.content_type == SiteBlock.ContentType.TEXT:
                block.text_html = (
                    self.cleaned_data.get(block_field_name(page, key, 'text_html'), '') or ''
                ).strip()
            elif block.content_type == SiteBlock.ContentType.IMAGE:
                uploaded = self.cleaned_data.get(block_field_name(page, key, 'image'))
                if uploaded:
                    block.image = uploaded
            block.save()
        cache.delete(SITE_BLOCKS_CACHE_KEY)


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = (
            'title', 'subtitle', 'image',
            'cta_primary_label', 'cta_primary_url',
            'cta_secondary_label', 'cta_secondary_url',
            'sort_order', 'is_active',
        )


HeroSlideFormSet = forms.modelformset_factory(
    HeroSlide, form=HeroSlideForm, extra=1, can_delete=True,
)


class HistorySlideForm(forms.ModelForm):
    class Meta:
        model = HistorySlide
        fields = (
            'year_label', 'title', 'text', 'image',
            'cta_label', 'cta_url',
            'sort_order', 'is_active',
        )
        widgets = {
            'year_label': CmsAdminTextInputWidget(),
            'title': CmsAdminTextInputWidget(),
            'text': CmsAdminTextareaWidget(attrs={'rows': 4}),
            'cta_label': CmsAdminTextInputWidget(),
            'cta_url': CmsAdminTextInputWidget(),
        }


HistorySlideFormSet = forms.modelformset_factory(
    HistorySlide, form=HistorySlideForm, extra=1, can_delete=True,
)


def site_content_section_view(request, page_slug: str, section_slug: str, model_admin=None):
    section = get_section(page_slug, section_slug)
    if section is None:
        raise Http404
    SiteSettings.load()
    blocks = load_section_blocks(section)
    form = SitePageContentForm(section, blocks, request.POST or None, request.FILES or None)
    hero_formset = None
    history_formset = None
    if section.slug == 'hero':
        hero_formset = HeroSlideFormSet(
            request.POST or None,
            request.FILES or None,
            queryset=HeroSlide.objects.all(),
            prefix='hero_slides',
        )
    if section.slug == 'about':
        history_formset = HistorySlideFormSet(
            request.POST or None,
            request.FILES or None,
            queryset=HistorySlide.objects.all(),
            prefix='history_slides',
        )

    if request.method == 'POST':
        ok = form.is_valid()
        if hero_formset is not None:
            ok = ok and hero_formset.is_valid()
        if history_formset is not None:
            ok = ok and history_formset.is_valid()
        if ok:
            form.save()
            if hero_formset is not None:
                hero_formset.save()
            if history_formset is not None:
                history_formset.save()
            messages.success(request, 'Збережено')
            return HttpResponseRedirect(request.path)

    return render(
        request,
        'admin/core/site_content_page.html',
        {
            **(model_admin.admin_site.each_context(request) if model_admin else {}),
            'title': section.title,
            'section': section,
            'form': form,
            'hero_formset': hero_formset,
            'history_formset': history_formset,
            'opts': getattr(model_admin, 'opts', None),
        },
    )
