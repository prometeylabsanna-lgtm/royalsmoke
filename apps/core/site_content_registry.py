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
    preview_url: str = '/'
    description: str = ''
    visibility_key: str = ''
    field_groups: tuple[FieldGroup, ...] = field(default_factory=tuple)
    admin_model_name: str = ''


CONTENT_SECTIONS: tuple[ContentSection, ...] = (
    ContentSection(
        slug='hero',
        page_slug='home',
        title='Головний банер',
        sidebar_title='Головна — Hero',
        sidebar_icon='image',
        preview_url='/',
        admin_model_name='homeherosettings',
        visibility_key='hero_section_visible',
        description='Мітка hero та слайди (слайди — окремим formset).',
        blocks=(('home', 'hero_eyebrow'),),
        field_groups=(FieldGroup('Мітка', ('hero_eyebrow',)),),
    ),
    ContentSection(
        slug='categories',
        page_slug='home',
        title='Ключові категорії',
        sidebar_title='Головна — Категорії',
        sidebar_icon='category',
        preview_url='/#categories',
        admin_model_name='homecategoriessettings',
        visibility_key='categories_section_visible',
        blocks=(('home', 'categories_title'),),
        field_groups=(FieldGroup('Заголовок', ('categories_title',)),),
    ),
    ContentSection(
        slug='top',
        page_slug='home',
        title='Топ продажів',
        sidebar_title='Головна — Топ',
        sidebar_icon='trending_up',
        preview_url='/#top',
        admin_model_name='hometopsettings',
        visibility_key='top_section_visible',
        blocks=(('home', 'top_title'),),
        field_groups=(FieldGroup('Заголовок', ('top_title',)),),
    ),
    ContentSection(
        slug='new',
        page_slug='home',
        title='Новинки',
        sidebar_title='Головна — Новинки',
        sidebar_icon='new_releases',
        preview_url='/#new',
        admin_model_name='homenewsettings',
        visibility_key='new_section_visible',
        blocks=(('home', 'new_title'),),
        field_groups=(FieldGroup('Заголовок', ('new_title',)),),
    ),
    ContentSection(
        slug='about',
        page_slug='home',
        title='Історія сигар',
        sidebar_title='Головна — Історія сигар',
        sidebar_icon='menu_book',
        preview_url='/#home-history',
        admin_model_name='homeaboutsettings',
        visibility_key='about_section_visible',
        description='Мітка, фон і слайди timeline (слайди — окремим formset).',
        blocks=(('home', 'about_kicker'), ('home', 'about_bg')),
        field_groups=(
            FieldGroup('Секція', ('about_kicker',)),
            FieldGroup('Фон', ('about_bg',)),
        ),
    ),
    ContentSection(
        slug='service',
        page_slug='home',
        title='Сервіс',
        sidebar_title='Головна — Сервіс',
        sidebar_icon='room_service',
        preview_url='/#service',
        admin_model_name='homeservicesettings',
        visibility_key='service_section_visible',
        blocks=(
            ('home', 'service_kicker'),
            ('service', 'booking_title'),
            ('service', 'booking_lead'),
            ('service', 'calculator_title'),
            ('service', 'calculator_lead'),
            ('service', 'b2b_title'),
            ('service', 'b2b_lead'),
            ('service', 'delivery_title'),
            ('service', 'delivery_lead'),
        ),
        field_groups=(
            FieldGroup('Kicker', ('service_kicker',)),
            FieldGroup('Бронювання', ('booking_title', 'booking_lead')),
            FieldGroup('Калькулятор', ('calculator_title', 'calculator_lead')),
            FieldGroup('B2B', ('b2b_title', 'b2b_lead')),
            FieldGroup('Доставка', ('delivery_title', 'delivery_lead')),
        ),
    ),
    ContentSection(
        slug='header',
        page_slug='site',
        title='Header / пошук',
        sidebar_title='Меню навігації',
        sidebar_icon='web',
        preview_url='/',
        admin_model_name='siteheadersettings',
        blocks=(('site', 'header_search_placeholder'),),
        field_groups=(FieldGroup('Пошук', ('header_search_placeholder',)),),
    ),
    ContentSection(
        slug='footer',
        page_slug='site',
        title='Footer',
        sidebar_title='Footer',
        sidebar_icon='vertical_align_bottom',
        preview_url='/',
        admin_model_name='sitefootersettings',
        blocks=(('site', 'footer_tagline'),),
        field_groups=(FieldGroup('Слоган', ('footer_tagline',)),),
    ),
)


def get_section(page_slug: str, section_slug: str) -> ContentSection | None:
    for section in CONTENT_SECTIONS:
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


def build_content_sidebar_items() -> list[dict]:
    items = []
    for section in CONTENT_SECTIONS:
        if not section.admin_model_name:
            continue
        items.append({
            'title': section.sidebar_title or section.title,
            'icon': section.sidebar_icon,
            'link': f'core/{section.admin_model_name}/',
        })
    return items
