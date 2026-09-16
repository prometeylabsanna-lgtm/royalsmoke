from __future__ import annotations

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from apps.core.block_defaults import BLOCK_DEFAULTS

register = template.Library()


def _blocks(context):
    return context.get('site_blocks') or {}


@register.simple_tag(takes_context=True)
def cms_text(context, page, key, fallback=''):
    fn = context.get('block_text')
    if callable(fn):
        value = fn(page, key, fallback)
        if value:
            return value
    block = _blocks(context).get(f'{page}.{key}')
    if block and block.text_html:
        return block.text_html
    default = BLOCK_DEFAULTS.get((page, key), fallback)
    return str(default or fallback)


@register.simple_tag(takes_context=True)
def cms_visible(context, page, key, default=True):
    fn = context.get('block_visible')
    if callable(fn):
        return fn(page, key, default)
    raw = str(cms_text(context, page, key, '1' if default else '0'))
    return raw.strip() in {'1', 'true', 'True', ''}


@register.simple_tag(takes_context=True)
def cms_image(context, page, key):
    block = _blocks(context).get(f'{page}.{key}')
    if block and getattr(block, 'image', None):
        try:
            return block.image.url
        except ValueError:
            return ''
    return ''


@register.filter
def cms_format(value, arg):
    return str(value or '').replace('{name}', str(arg))


@register.filter
def cms_lines(value):
    text = escape(str(value or '')).replace('\r\n', '\n').replace('\n', '<br>')
    return mark_safe(text)
