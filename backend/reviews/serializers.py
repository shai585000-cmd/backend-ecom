from rest_framework import serializers
from .models import Review
from backend.orders.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'product', 'rating', 
            'title', 'comment', 'is_verified_purchase', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'is_verified_purchase', 'created_at', 'updated_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'title', 'comment']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit etre entre 1 et 5")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        
        # Verifier si l'utilisateur a deja laisse un avis
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError(
                {"error": "Vous avez deja laisse un avis pour ce produit"}
            )
        
        # Verifier si c'est un achat verifie
        is_verified = Order.objects.filter(
            user=user,
            items__product=product,
            status='delivered'
        ).exists()
        
        review = Review.objects.create(
            user=user,
            is_verified_purchase=is_verified,
            **validated_data
        )
        return review


class ProductReviewStatsSerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    rating_distribution = serializers.DictField()
