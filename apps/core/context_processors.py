from django.core.cache import cache
from django.utils.translation import get_language

from apps.core.block_defaults import BLOCK_DEFAULTS
from apps.core.breadcrumbs import build_breadcrumbs
from apps.core.currency import get_currency
from apps.core.cms_text_normalize import normalize_cms_plain
from apps.core.models import HeroSlide, HistorySlide, SiteBlock, SiteSettings
from apps.core.page_styles import get_chrome_style_vars, get_page_style_vars


def site_globals(request):
    lang = get_language() or 'uk'
    settings_key = f'site_settings:{lang}'
    blocks_key = f'site_blocks:{lang}'

    settings_obj = cache.get(settings_key)
    if settings_obj is None:
        settings_obj = SiteSettings.load()
        cache.set(settings_key, settings_obj, 300)

    blocks = cache.get(blocks_key)
    if blocks is None:
        blocks = {}
        for b in SiteBlock.objects.filter(is_active=True):
            blocks[f'{b.page}.{b.key}'] = b
        cache.set(blocks_key, blocks, 300)

    def block_text(page: str, key: str, default: str = '') -> str:
        b = blocks.get(f'{page}.{key}')
        if b and b.text_html:
            return b.text_html
        return str(BLOCK_DEFAULTS.get((page, key), default))

    def block_visible(page: str, key: str, default: bool = True) -> bool:
        raw = normalize_cms_plain(str(block_text(page, key, '1' if default else '0')))
        return raw.strip() in {'1', 'true', 'True', ''}

    hero_slides = list(HeroSlide.objects.filter(is_active=True))
    history_slides = list(HistorySlide.objects.filter(is_active=True))
    page_style = get_page_style_vars(request)
    chrome_style = get_chrome_style_vars()

    return {
        'site_settings': settings_obj,
        'site_blocks': blocks,
        'block_text': block_text,
        'block_visible': block_visible,
        'hero_slides': hero_slides,
        'history_slides': history_slides,
        'page_style': page_style,
        'page_background_color': page_style.get('bg', ''),
        'chrome_style': chrome_style,
        'current_language': get_language() or 'uk',
        'currency': get_currency(),
        'age_gate_cookie': 'age_ok',
        'breadcrumbs': build_breadcrumbs(request),
    }
