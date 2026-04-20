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
        fields = ['id', 'image', 'images', 'user', 'categorie', 'categorie_id', 'promotion', 'promotion_price', 'name', 'description', 'price', 'is_featured', 'created_at', 'updated_at']
    
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
        
        # Essayer d'obtenir l'URL via le storage (fonctionne avec Cloudinary)
        try:
            return obj.image.url
        except Exception:
            pass
        
        # Sinon retourner tel quel (chemin local)
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/media/{image_str}')
        return image_str

    def get_images(self, obj):
        """Retourne toutes les images sous forme de tableau"""
        images = []
        image_fields = ['image', 'image_2', 'image_3', 'image_4']
        
        for idx, field in enumerate(image_fields):
            img_field = getattr(obj, field, None)
            if img_field:
                img_str = str(img_field)
                
                # Même logique que get_image pour l'URL
                if 'https%3A' in img_str or 'http%3A' in img_str:
                    url = unquote(img_str)
                    if url.startswith('/media/'):
                        url = url[7:]
                    images.append({'id': idx, 'image': url})
                elif img_str.startswith('http://') or img_str.startswith('https://'):
                    images.append({'id': idx, 'image': img_str})
                else:
                    try:
                        url = img_field.url
                        images.append({'id': idx, 'image': url})
                    except Exception:
                        request = self.context.get('request')
                        if request:
                            url = request.build_absolute_uri(f'/media/{img_str}')
                            images.append({'id': idx, 'image': url})
                        else:
                            images.append({'id': idx, 'image': f'/media/{img_str}'})
        
        return images if images else None
