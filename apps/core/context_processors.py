from django.core.cache import cache
from django.utils.translation import get_language

from apps.core.block_defaults import BLOCK_DEFAULTS
from apps.core.breadcrumbs import build_breadcrumbs
from apps.core.models import HeroSlide, HistorySlide, SiteBlock, SiteSettings


def site_globals(request):
    settings_obj = cache.get('site_settings')
    if settings_obj is None:
        settings_obj = SiteSettings.load()
        cache.set('site_settings', settings_obj, 300)

    blocks = cache.get('site_blocks')
    if blocks is None:
        blocks = {}
        for b in SiteBlock.objects.filter(is_active=True):
            blocks[f'{b.page}.{b.key}'] = b
        cache.set('site_blocks', blocks, 300)

    def block_text(page: str, key: str, default: str = '') -> str:
        b = blocks.get(f'{page}.{key}')
        if b and b.text_html:
            return b.text_html
        return str(BLOCK_DEFAULTS.get((page, key), default))

    def block_visible(page: str, key: str, default: bool = True) -> bool:
        raw = str(block_text(page, key, '1' if default else '0'))
        return raw.strip() in {'1', 'true', 'True', ''}

    hero_slides = list(HeroSlide.objects.filter(is_active=True))
    history_slides = list(HistorySlide.objects.filter(is_active=True))

    return {
        'site_settings': settings_obj,
        'site_blocks': blocks,
        'block_text': block_text,
        'block_visible': block_visible,
        'hero_slides': hero_slides,
        'history_slides': history_slides,
        'current_language': get_language() or 'uk',
        'age_gate_cookie': 'age_ok',
        'breadcrumbs': build_breadcrumbs(request),
    }
