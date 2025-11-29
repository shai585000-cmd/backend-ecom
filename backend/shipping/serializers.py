from rest_framework import serializers
from .models import ShippingAddress, ShippingZone


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'id',
            'full_name',
            'phone',
            'address',
            'city',
            'neighborhood',
            'postal_code',
            'country',
            'is_default',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class ShippingAddressCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'phone',
            'address',
            'city',
            'neighborhood',
            'postal_code',
            'country',
            'is_default',
        ]


class ShippingZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingZone
        fields = [
            'id',
            'name',
            'shipping_fee',
            'estimated_days',
            'is_active',
        ]
