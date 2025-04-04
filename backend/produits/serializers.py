from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','image','user', 'categorie', 'promotion', 'promotion_price', 'name', 'description', 'price', 'is_featured', 'created_at', 'updated_at']
