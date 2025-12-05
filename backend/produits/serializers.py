from rest_framework import serializers
from urllib.parse import unquote
from .models import Product
from backend.home.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    categorie = CategorySerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='categorie', 
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        fields = ['id', 'image', 'user', 'categorie', 'categorie_id', 'promotion', 'promotion_price', 'name', 'description', 'price', 'is_featured', 'created_at', 'updated_at']
    
    def get_image(self, obj):
        """Retourne l'URL d'image correcte"""
        if not obj.image:
            return None
        
        image_str = str(obj.image)
        
        # Si c'est une URL externe encodee dans /media/
        if 'https%3A' in image_str or 'http%3A' in image_str:
            # Decoder l'URL
            url = unquote(image_str)
            # Retirer /media/ si present
            if url.startswith('/media/'):
                url = url[7:]
            return url
        
        # Si c'est deja une URL complete
        if image_str.startswith('http://') or image_str.startswith('https://'):
            return image_str
        
        # Sinon retourner tel quel (chemin local)
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return image_str
