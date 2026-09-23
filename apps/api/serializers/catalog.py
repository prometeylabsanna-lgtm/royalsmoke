from rest_framework import serializers

from apps.catalog.models import Brand, Category, Product
from apps.core.currency import convert_from_uah, get_currency


def _money(value):
    if value is None:
        return None
    return convert_from_uah(value)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'kind', 'parent', 'image', 'description')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'country', 'logo', 'short_description')


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    display_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'sku', 'brand', 'category', 'short_story',
            'description', 'tasting_notes', 'wrapper', 'binder', 'filler',
            'country', 'strength', 'smoke_time', 'base_price', 'old_price',
            'currency', 'display_price', 'stock', 'video_url',
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['currency'] = get_currency()['code']
        data['base_price'] = str(_money(instance.base_price))
        data['old_price'] = (
            str(_money(instance.old_price)) if instance.old_price is not None else None
        )
        data['display_price'] = str(_money(instance.display_price))
        return data
