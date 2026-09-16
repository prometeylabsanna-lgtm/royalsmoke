from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from apps.core.block_defaults import BLOCK_FIELD_LABELS


@dataclass(frozen=True)
class FieldGroup:
    title: str
    block_keys: tuple[str, ...]


@dataclass(frozen=True)
class ContentSection:
    slug: str
    page_slug: str
    title: str
    blocks: tuple[tuple[str, str], ...]
    sidebar_title: str = ''
    sidebar_icon: str = 'edit_note'
    sidebar_group: str = 'home'
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''
    collection: str = ''


def _sections():
    from apps.core.site_content_sections import CONTENT_SECTIONS
    return CONTENT_SECTIONS


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in _sections():
        if section.page_slug == page_slug and section.slug == section_slug:
            return section
    return None


def iter_section_blocks(section: ContentSection) -> Iterator[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    if section.visibility_key:
        pair = (section.page_slug, section.visibility_key)
        yield pair
        seen.add(pair)
    for pair in section.blocks:
        if pair not in seen:
            yield pair
            seen.add(pair)


def get_block_field_label(page: str, key: str) -> str:
    return BLOCK_FIELD_LABELS.get((page, key), key)
