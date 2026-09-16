from __future__ import annotations

from django import forms
from unfold.widgets import UnfoldBooleanWidget

from apps.core.admin_site_content_widgets import (
    CmsAdminImageWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
)
from apps.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    INLINE_KEYS,
    MULTILINE_KEYS,
    is_visibility_key,
)
from apps.core.cms_i18n import CMS_LANGUAGES, iter_cms_langs
from apps.core.models import SiteBlock
from apps.core.site_content_registry import (
    ContentSection,
    get_block_field_label,
    iter_section_blocks,
)

SECTION_VISIBLE_FIELD = 'section_visible'


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
                'text_html': str(BLOCK_DEFAULTS.get(
                    (page, key), '1' if is_visibility_key(key) else '',
                )),
                'sort_order': 0,
                'is_active': True,
            },
        )
        if block.content_type != content_type:
            block.content_type = content_type
            block.save(update_fields=['content_type'])
        blocks[(page, key)] = block
    return blocks


def _lang_text(block: SiteBlock, attr: str) -> str:
    val = getattr(block, f'text_html_{attr}', None)
    if isinstance(val, str) and val.strip():
        return val
    if attr == 'uk':
        return block.text_html or ''
    return val or ''


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
        self.editor_groups = self._build_editor_groups()

    def _build_editor_groups(self) -> list[dict]:
        groups: list[dict] = []
        if SECTION_VISIBLE_FIELD in self.fields:
            groups.append({
                'title': 'Видимість',
                'rows': [{'kind': 'single', 'fields': [{'bound': self[SECTION_VISIBLE_FIELD], 'lang': ''}]}],
            })
        for group in self.section.field_groups:
            rows = []
            for key in group.block_keys:
                page = self.page_for_key(key)
                block = self.blocks[(page, key)]
                if is_visibility_key(key) and key != self.section.visibility_key:
                    rows.append({
                        'kind': 'single',
                        'fields': [{'bound': self[block_field_name(page, key, 'visible')], 'lang': ''}],
                    })
                elif block.content_type == SiteBlock.ContentType.IMAGE:
                    rows.append({
                        'kind': 'image',
                        'fields': [{'bound': self[block_field_name(page, key, 'image')], 'lang': ''}],
                    })
                else:
                    fields = [
                        {
                            'bound': self[block_field_name(page, key, f'text_html_{attr}')],
                            'lang': code,
                        }
                        for code, attr, _label in CMS_LANGUAGES
                    ]
                    rows.append({'kind': 'i18n', 'fields': fields})
            groups.append({'title': group.title, 'rows': rows})
        return groups

    def _visibility_page_key(self, section: ContentSection) -> tuple[str, str]:
        for page, key in iter_section_blocks(section):
            if key == section.visibility_key:
                return page, key
        raise KeyError(section.visibility_key)

    def page_for_key(self, key: str) -> str:
        for page, block_key in self.section.blocks:
            if block_key == key:
                return page
        return self.section.page_slug

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
            field = forms.ImageField(
                label=label,
                required=False,
                widget=CmsAdminImageWidget(),
            )
            field.initial = block.image
            self.fields[block_field_name(page, key, 'image')] = field
            return
        for code, attr, lang_label in iter_cms_langs():
            widget = (
                CmsAdminTextInputWidget(attrs={'data-cms-lang': code})
                if key in INLINE_KEYS
                else CmsAdminTextareaWidget(
                    attrs={
                        'rows': 4 if key in MULTILINE_KEYS else 2,
                        'data-cms-lang': code,
                    },
                )
            )
            self.fields[block_field_name(page, key, f'text_html_{attr}')] = forms.CharField(
                label=f'{label} ({lang_label})',
                initial=_lang_text(block, attr),
                required=False,
                widget=widget,
            )

    def save(self) -> None:
        if SECTION_VISIBLE_FIELD in self.fields:
            page, key = self._visibility_page_key(self.section)
            block = self.blocks[(page, key)]
            block.text_html = '1' if self.cleaned_data.get(SECTION_VISIBLE_FIELD) else '0'
            for _code, attr, _label in CMS_LANGUAGES:
                setattr(block, f'text_html_{attr}', block.text_html)
            block.is_active = True
            block.save()

        for block in self.blocks.values():
            page, key = block.page, block.key
            if key == self.section.visibility_key:
                continue
            if is_visibility_key(key):
                value = '1' if self.cleaned_data.get(
                    block_field_name(page, key, 'visible'),
                ) else '0'
                block.text_html = value
                for _code, attr, _label in CMS_LANGUAGES:
                    setattr(block, f'text_html_{attr}', value)
                block.is_active = True
                block.save()
                continue
            block.is_active = True
            if block.content_type == SiteBlock.ContentType.IMAGE:
                uploaded = self.cleaned_data.get(block_field_name(page, key, 'image'))
                if uploaded:
                    block.image = uploaded
            else:
                uk_val = ''
                for _code, attr, _label in CMS_LANGUAGES:
                    raw = (
                        self.cleaned_data.get(
                            block_field_name(page, key, f'text_html_{attr}'),
                        ) or ''
                    ).strip()
                    setattr(block, f'text_html_{attr}', raw)
                    if attr == 'uk':
                        uk_val = raw
                block.text_html = uk_val
            block.save()
