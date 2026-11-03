from __future__ import annotations

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.mobile.language import activate_mobile_language
from apps.mobile.models import MobileBrand, MobileLegalPage, MobileScreen, MobileSettings
from apps.mobile.serializers import (
    MobileBrandSerializer,
    MobileLegalPageSerializer,
    MobileScreenSerializer,
    MobileSettingsSerializer,
)


class _MobileLanguageMixin:
    def initial(self, request, *args, **kwargs):
        activate_mobile_language(request)
        super().initial(request, *args, **kwargs)


class MobileBrandViewSet(_MobileLanguageMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileBrandSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            MobileBrand.objects.filter(is_active=True)
            .prefetch_related('facts', 'lines', 'photos')
            .order_by('sort_order', 'name')
        )


class MobileScreenViewSet(_MobileLanguageMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileScreenSerializer
    permission_classes = [AllowAny]
    lookup_field = 'key'

    def get_queryset(self):
        return MobileScreen.objects.filter(is_active=True).prefetch_related('house_blocks')


class MobileLegalPageViewSet(_MobileLanguageMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileLegalPageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return MobileLegalPage.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_settings_view(request):
    lang = activate_mobile_language(request)
    settings_obj = MobileSettings.load()
    response = Response(MobileSettingsSerializer(settings_obj, context={'request': request}).data)
    response['Content-Language'] = lang
    return response


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_bundle_view(request):
    lang = activate_mobile_language(request)
    ctx = {'request': request}
    brands = (
        MobileBrand.objects.filter(is_active=True)
        .prefetch_related('facts', 'lines', 'photos')
        .order_by('sort_order', 'name')
    )
    screens = MobileScreen.objects.filter(is_active=True).prefetch_related('house_blocks')
    pages = MobileLegalPage.objects.filter(is_active=True)
    response = Response({
        'settings': MobileSettingsSerializer(MobileSettings.load(), context=ctx).data,
        'brands': MobileBrandSerializer(brands, many=True, context=ctx).data,
        'screens': {
            s.key: MobileScreenSerializer(s, context=ctx).data
            for s in screens
        },
        'pages': {
            p.slug: MobileLegalPageSerializer(p, context=ctx).data
            for p in pages
        },
    })
    response['Content-Language'] = lang
    return response
