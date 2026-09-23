from __future__ import annotations

from django.contrib import messages
from django.core.cache import cache
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from apps.core.admin_collection_formsets import (
    DeliveryPaymentFormSet,
    DeliveryRegionFormSet,
    HeroSlideFormSet,
    HistorySlideFormSet,
    HomeBrandCardFormSet,
)
from apps.core.admin_site_content_form import SitePageContentForm, load_section_blocks
from apps.core.delivery_cards import ensure_delivery_cards
from apps.core.models import (
    DeliveryCard,
    HeroSlide,
    HistorySlide,
    HomeBrandCard,
    SiteSettings,
    clear_site_content_cache,
)
from apps.core.site_content_registry import get_section

SITE_BLOCKS_CACHE_KEY = 'site_blocks'


def _formsets_for(section, request):
    packs = []
    if section.collection == 'hero':
        packs.append(('hero_formset', HeroSlideFormSet, HeroSlide.objects.all(), 'hero_slides'))
    if section.collection == 'history':
        packs.append(('history_formset', HistorySlideFormSet, HistorySlide.objects.all(), 'history_slides'))
    if section.collection == 'brands':
        packs.append((
            'brand_formset', HomeBrandCardFormSet,
            HomeBrandCard.objects.select_related('brand'), 'brand_cards',
        ))
    if section.collection == 'delivery':
        ensure_delivery_cards()
        packs.append((
            'delivery_region_formset',
            DeliveryRegionFormSet,
            DeliveryCard.objects.filter(kind=DeliveryCard.Kind.REGION),
            'delivery_regions',
        ))
        packs.append((
            'delivery_payment_formset',
            DeliveryPaymentFormSet,
            DeliveryCard.objects.filter(kind=DeliveryCard.Kind.PAYMENT),
            'delivery_payments',
        ))
    built = {}
    for key, factory, qs, prefix in packs:
        built[key] = factory(
            request.POST or None,
            request.FILES or None,
            queryset=qs,
            prefix=prefix,
        )
    return built


def site_content_section_view(request, page_slug: str, section_slug: str, model_admin=None):
    section = get_section(page_slug, section_slug)
    if section is None:
        raise Http404
    SiteSettings.load()
    blocks = load_section_blocks(section)
    form = SitePageContentForm(section, blocks, request.POST or None, request.FILES or None)
    extra_sets = _formsets_for(section, request)

    if request.method == 'POST':
        ok = form.is_valid() and all(fs.is_valid() for fs in extra_sets.values())
        if ok:
            form.save()
            for fs in extra_sets.values():
                fs.save()
            cache.delete(SITE_BLOCKS_CACHE_KEY)
            clear_site_content_cache()
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
            'hero_formset': extra_sets.get('hero_formset'),
            'history_formset': extra_sets.get('history_formset'),
            'brand_formset': extra_sets.get('brand_formset'),
            'delivery_region_formset': extra_sets.get('delivery_region_formset'),
            'delivery_payment_formset': extra_sets.get('delivery_payment_formset'),
            'opts': getattr(model_admin, 'opts', None),
        },
    )
