from __future__ import annotations

from django import forms
from unfold.widgets import UnfoldBooleanWidget

from apps.core.admin_site_content_widgets import (
    CmsAdminFileWidget,
    CmsAdminImageWidget,
    CmsAdminTextInputWidget,
    CmsAdminTextareaWidget,
    CmsAdminTinyMCEWidget,
)
from apps.core.block_defaults import (
    BLOCK_CONTENT_TYPES,
    BLOCK_DEFAULTS,
    INLINE_KEYS,
    MULTILINE_KEYS,
    is_visibility_key,
)
from apps.core.cms_i18n import CMS_LANGUAGES, iter_cms_langs
from apps.core.cms_text_normalize import sanitize_cms_storage
from apps.core.models import SiteBlock, SiteSettings
from apps.core.site_content_registry import (
    ContentSection,
    get_block_field_label,
    iter_section_blocks,
)
from apps.core.validation.admin_forms import clean_optional_url
from apps.core.validation.fields import EmailField, PhoneField

SECTION_VISIBLE_FIELD = 'section_visible'
SETTINGS_FIELD_PREFIX = 'settings__'
SETTINGS_FIELD_LABELS = {
    'site_name': 'Назва бренду',
    'phone': 'Телефон',
    'email': 'Email',
}
# TinyMCE лише для навмисного HTML (юридичні body тощо). Решта — textarea,
# інакше редактор обгортає підписи в <p> і теги світяться на вітрині.
TINYMCE_KEYS = frozenset({'body'})


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
        self._settings = SiteSettings.load() if section.settings_fields else None

        if section.visibility_key:
            page, key = self._visibility_page_key(section)
            block = blocks[(page, key)]
            self.fields[SECTION_VISIBLE_FIELD] = forms.BooleanField(
                label='Показувати секцію на сайті',
                required=False,
                initial=block.text_html.strip() in {'1', 'true', 'True'},
                widget=UnfoldBooleanWidget(),
            )

        self._add_settings_fields()
        for page, key in section.blocks:
            self._add_block_fields(blocks[(page, key)])
        self.editor_groups = self._build_editor_groups()

    def _settings_field_name(self, name: str) -> str:
        return f'{SETTINGS_FIELD_PREFIX}{name}'

    def _add_settings_fields(self) -> None:
        if not self._settings:
            return
        for name in self.section.settings_fields:
            label = SETTINGS_FIELD_LABELS.get(name, name)
            initial = getattr(self._settings, name, '') or ''
            if name == 'phone':
                self.fields[self._settings_field_name(name)] = PhoneField(
                    label=label,
                    optional=True,
                    initial=initial,
                    widget=CmsAdminTextInputWidget(),
                )
            elif name == 'email':
                self.fields[self._settings_field_name(name)] = EmailField(
                    label=label,
                    optional=True,
                    initial=initial,
                    widget=CmsAdminTextInputWidget(),
                )
            else:
                self.fields[self._settings_field_name(name)] = forms.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=100,
                    widget=CmsAdminTextInputWidget(),
                )

    def _build_editor_groups(self) -> list[dict]:
        groups: list[dict] = []
        if SECTION_VISIBLE_FIELD in self.fields:
            groups.append({
                'title': 'Видимість',
                'rows': [{'kind': 'single', 'fields': [{'bound': self[SECTION_VISIBLE_FIELD], 'lang': ''}]}],
            })
        if self.section.settings_fields:
            groups.append({
                'title': 'Бренд і контакти',
                'rows': [
                    {
                        'kind': 'single',
                        'fields': [{'bound': self[self._settings_field_name(name)], 'lang': ''}],
                    }
                    for name in self.section.settings_fields
                    if self._settings_field_name(name) in self.fields
                ],
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
                elif block.content_type == SiteBlock.ContentType.URL:
                    rows.append({
                        'kind': 'url',
                        'fields': [
                            {'bound': self[block_field_name(page, key, 'link_url')], 'lang': ''},
                            {'bound': self[block_field_name(page, key, 'link_label')], 'lang': ''},
                        ],
                    })
                elif block.content_type == SiteBlock.ContentType.VIDEO:
                    rows.append({
                        'kind': 'video',
                        'fields': [
                            {'bound': self[block_field_name(page, key, 'video_embed_url')], 'lang': ''},
                            {'bound': self[block_field_name(page, key, 'video_file')], 'lang': ''},
                        ],
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
        if block.content_type == SiteBlock.ContentType.URL:
            self.fields[block_field_name(page, key, 'link_url')] = forms.CharField(
                label=f'{label} — URL',
                required=False,
                initial=block.link_url or '',
                widget=CmsAdminTextInputWidget(),
            )
            self.fields[block_field_name(page, key, 'link_label')] = forms.CharField(
                label=f'{label} — текст',
                required=False,
                initial=block.link_label or '',
                widget=CmsAdminTextInputWidget(),
            )
            return
        if block.content_type == SiteBlock.ContentType.VIDEO:
            self.fields[block_field_name(page, key, 'video_embed_url')] = forms.URLField(
                label=f'{label} — embed URL',
                required=False,
                initial=block.video_embed_url or '',
                widget=CmsAdminTextInputWidget(),
            )
            file_field = forms.FileField(
                label=f'{label} — файл',
                required=False,
                widget=CmsAdminFileWidget(),
            )
            file_field.initial = block.video_file
            self.fields[block_field_name(page, key, 'video_file')] = file_field
            return
        use_tinymce = key in TINYMCE_KEYS
        for code, attr, lang_label in iter_cms_langs():
            if key in INLINE_KEYS:
                widget = CmsAdminTextInputWidget(attrs={'data-cms-lang': code})
            elif use_tinymce:
                widget = CmsAdminTinyMCEWidget(attrs={'data-cms-lang': code})
            else:
                widget = CmsAdminTextareaWidget(
                    attrs={
                        'rows': 4 if key in MULTILINE_KEYS else 2,
                        'data-cms-lang': code,
                    },
                )
            self.fields[block_field_name(page, key, f'text_html_{attr}')] = forms.CharField(
                label=f'{label} ({lang_label})',
                initial=_lang_text(block, attr),
                required=False,
                widget=widget,
            )

    def save(self) -> None:
        if self._settings and self.section.settings_fields:
            for name in self.section.settings_fields:
                fname = self._settings_field_name(name)
                if fname not in self.cleaned_data:
                    continue
                value = self.cleaned_data.get(fname)
                if value is None:
                    value = ''
                setattr(self._settings, name, str(value).strip())
            self._settings.save()

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
            elif block.content_type == SiteBlock.ContentType.URL:
                block.link_url = clean_optional_url(
                    self.cleaned_data.get(block_field_name(page, key, 'link_url'), '') or '',
                )
                block.link_label = (
                    self.cleaned_data.get(block_field_name(page, key, 'link_label'), '') or ''
                ).strip()
            elif block.content_type == SiteBlock.ContentType.VIDEO:
                embed = (
                    self.cleaned_data.get(block_field_name(page, key, 'video_embed_url'), '') or ''
                ).strip()
                block.video_embed_url = embed
                uploaded = self.cleaned_data.get(block_field_name(page, key, 'video_file'))
                if uploaded:
                    block.video_file = uploaded
            else:
                uk_val = ''
                for _code, attr, _label in CMS_LANGUAGES:
                    raw = (
                        self.cleaned_data.get(
                            block_field_name(page, key, f'text_html_{attr}'),
                        ) or ''
                    ).strip()
                    cleaned = sanitize_cms_storage(key, raw)
                    setattr(block, f'text_html_{attr}', cleaned)
                    if attr == 'uk':
                        uk_val = cleaned
                block.text_html = uk_val
            block.save()
