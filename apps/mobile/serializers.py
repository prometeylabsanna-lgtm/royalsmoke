from __future__ import annotations

from rest_framework import serializers

from apps.mobile.models import (
    MobileBrand,
    MobileBrandFact,
    MobileBrandLine,
    MobileBrandPhoto,
    MobileHouseBlock,
    MobileLegalPage,
    MobileScreen,
    MobileSettings,
)


def _abs_url(request, filefield) -> str:
    if not filefield:
        return ''
    try:
        url = filefield.url
    except (ValueError, AttributeError):
        return ''
    if not url:
        return ''
    if request is None:
        return url
    return request.build_absolute_uri(url)


class MobileBrandFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileBrandFact
        fields = ('label', 'value', 'sort_order')


class MobileBrandLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileBrandLine
        fields = ('name', 'sort_order')


class MobileBrandPhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = MobileBrandPhoto
        fields = ('image', 'sort_order')

    def get_image(self, obj):
        return _abs_url(self.context.get('request'), obj.image)


class MobileBrandSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug')
    cover = serializers.SerializerMethodField()
    facts = MobileBrandFactSerializer(many=True, read_only=True)
    lines = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = MobileBrand
        fields = (
            'id', 'slug', 'name', 'short_name', 'mono', 'country', 'panel',
            'cover', 'heritage', 'sort_order', 'facts', 'lines', 'photos',
        )

    def get_cover(self, obj):
        return _abs_url(self.context.get('request'), obj.cover)

    def get_lines(self, obj):
        return [line.name for line in obj.lines.all()]

    def get_photos(self, obj):
        qs = obj.photos.filter(is_active=True)
        return MobileBrandPhotoSerializer(qs, many=True, context=self.context).data


class MobileHouseBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileHouseBlock
        fields = ('index_label', 'title', 'body', 'sort_order')


class MobileScreenSerializer(serializers.ModelSerializer):
    hero_image = serializers.SerializerMethodField()
    house_blocks = serializers.SerializerMethodField()

    class Meta:
        model = MobileScreen
        fields = (
            'key', 'kicker', 'title', 'subtitle', 'body', 'body_secondary',
            'cta_primary', 'cta_secondary', 'confirm_label', 'legal_note',
            'success_title', 'success_body', 'hero_image', 'house_blocks',
        )

    def get_hero_image(self, obj):
        return _abs_url(self.context.get('request'), obj.hero_image)

    def get_house_blocks(self, obj):
        if obj.key != MobileScreen.Key.HOUSE:
            return []
        return MobileHouseBlockSerializer(obj.house_blocks.all(), many=True).data


class MobileLegalPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileLegalPage
        fields = ('slug', 'title', 'body')


class MobileSettingsSerializer(serializers.ModelSerializer):
    app_seal = serializers.SerializerMethodField()

    class Meta:
        model = MobileSettings
        fields = (
            'app_version', 'app_blurb', 'app_seal',
            'contact_address', 'contact_phone', 'contact_hours',
            'contact_lat', 'contact_lng',
        )

    def get_app_seal(self, obj):
        return _abs_url(self.context.get('request'), obj.app_seal)
