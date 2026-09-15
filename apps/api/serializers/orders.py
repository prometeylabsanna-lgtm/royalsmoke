from rest_framework import serializers

from apps.orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'product_name', 'variant_name', 'product_sku',
            'price', 'quantity', 'line_total',
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'order_number', 'status', 'total', 'currency', 'created_at',
            'delivery_service', 'payment_method',
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'order_number', 'status', 'subtotal', 'discount', 'delivery_cost',
            'total', 'currency', 'created_at',
            'delivery_service', 'delivery_city', 'delivery_address',
            'np_city_ref', 'np_warehouse_ref', 'np_ttn',
            'payment_method', 'first_name', 'last_name', 'phone', 'email',
            'comment', 'items',
        )


class CheckoutSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=30)
    email = serializers.EmailField()
    delivery_service = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES)
    delivery_city = serializers.CharField(max_length=150)
    delivery_address = serializers.CharField(max_length=255)
    np_city_ref = serializers.CharField(required=False, allow_blank=True, max_length=64)
    np_warehouse_ref = serializers.CharField(required=False, allow_blank=True, max_length=64)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES)
    comment = serializers.CharField(required=False, allow_blank=True)
    delivery_cost = serializers.DecimalField(
        required=False, max_digits=12, decimal_places=2, min_value=0, default=0,
    )
    age_confirm = serializers.BooleanField()

    def validate_age_confirm(self, value):
        if not value:
            raise serializers.ValidationError('Age confirmation required')
        return value

    def validate(self, attrs):
        if attrs.get('delivery_service') == Order.DELIVERY_NP:
            if not attrs.get('np_city_ref') or not attrs.get('np_warehouse_ref'):
                raise serializers.ValidationError(
                    {'delivery_address': 'Select NP city and warehouse'}
                )
        return attrs
