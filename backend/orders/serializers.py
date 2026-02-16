from rest_framework import serializers
from .models import Order, OrderItem
from backend.produits.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_details',
            'product_name',
            'quantity',
            'unit_price',
            'total_price',
        ]
        read_only_fields = ['product_name', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user',
            'user_email',
            'status',
            'status_display',
            'total_amount',
            'shipping_address',
            'shipping_city',
            'shipping_phone',
            'notes',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user', 'order_number', 'total_amount', 'created_at', 'updated_at']


class OrderItemCreateSerializer(serializers.Serializer):
    """Serializer pour un item de commande envoyé depuis le frontend"""
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderCreateSerializer(serializers.Serializer):
    """Serializer pour créer une commande avec les items du panier"""
    shipping_address = serializers.CharField(max_length=500)
    shipping_city = serializers.CharField(max_length=100)
    shipping_phone = serializers.CharField(max_length=20)
    notes = serializers.CharField(required=False, allow_blank=True)
    guest_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    guest_email = serializers.EmailField(required=False, allow_blank=True)
    items = OrderItemCreateSerializer(many=True)


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer pour mettre à jour le statut d'une commande"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
