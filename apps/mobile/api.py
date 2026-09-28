from __future__ import annotations

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.mobile.models import MobileBrand, MobileLegalPage, MobileScreen, MobileSettings
from apps.mobile.serializers import (
    MobileBrandSerializer,
    MobileLegalPageSerializer,
    MobileScreenSerializer,
    MobileSettingsSerializer,
)


class MobileBrandViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileBrandSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            MobileBrand.objects.filter(is_active=True)
            .prefetch_related('facts', 'lines', 'photos')
            .order_by('sort_order', 'name')
        )


class MobileScreenViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileScreenSerializer
    permission_classes = [AllowAny]
    lookup_field = 'key'

    def get_queryset(self):
        return MobileScreen.objects.filter(is_active=True).prefetch_related('house_blocks')


class MobileLegalPageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MobileLegalPageSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        return MobileLegalPage.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_settings_view(request):
    settings_obj = MobileSettings.load()
    return Response(MobileSettingsSerializer(settings_obj, context={'request': request}).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_bundle_view(request):
    ctx = {'request': request}
    brands = (
        MobileBrand.objects.filter(is_active=True)
        .prefetch_related('facts', 'lines', 'photos')
        .order_by('sort_order', 'name')
    )
    screens = MobileScreen.objects.filter(is_active=True).prefetch_related('house_blocks')
    pages = MobileLegalPage.objects.filter(is_active=True)
    return Response({
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
