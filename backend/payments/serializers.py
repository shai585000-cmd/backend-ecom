from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'order',
            'transaction_id',
            'payment_method',
            'payment_method_display',
            'amount',
            'status',
            'status_display',
            'phone_number',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['transaction_id', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.Serializer):
    """Serializer pour créer un paiement"""
    order_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=['mobile_money', 'orange_money', 'cash'])
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate(self, data):
        # Le numéro de téléphone est requis pour Mobile Money
        if data['payment_method'] in ['mobile_money', 'orange_money']:
            if not data.get('phone_number'):
                raise serializers.ValidationError({
                    'phone_number': 'Le numéro de téléphone est requis pour le paiement Mobile Money'
                })
        return data
