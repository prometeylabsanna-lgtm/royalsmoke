from rest_framework import serializers

from apps.catalog.models import Brand, Category, Product, ProductVariant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'kind', 'parent', 'image', 'description')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'country', 'logo', 'short_description')


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = (
            'id', 'name', 'slug', 'length_mm', 'ring_gauge', 'shape',
            'price', 'old_price', 'sku', 'stock', 'image',
        )


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variants = VariantSerializer(many=True, read_only=True)
    display_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'sku', 'brand', 'category', 'short_story',
            'description', 'tasting_notes', 'wrapper', 'binder', 'filler',
            'country', 'strength', 'smoke_time', 'base_price', 'old_price',
            'currency', 'display_price', 'variants', 'video_url',
        )
