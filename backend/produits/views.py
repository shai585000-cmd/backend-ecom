# Imports Django
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

# Imports Django REST Framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser

# Imports internes
from .models import Product
from .serializers import ProductSerializer
from .recommendation_utils import get_recommended_products

# Obtenir le modèle User personnalisé
User = get_user_model()

# View pour lister tous les produits
class ProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.filter(promotion=False)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# View pour les détails d'un produit spécifique
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_object(self):
        # Récupère l'ID à partir des paramètres d'URL
        product_id = self.kwargs.get('id')
        # Récupère l'objet Product ou renvoie une erreur 404 si non trouvé
        product = get_object_or_404(Product, id=product_id)

        # Incrémente les vues uniquement pour les requêtes GET
        if self.request.method == 'GET':
            product.views += 1
            product.save()

        return product

# View pour les produits en vedette
class FeaturedProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        featured_products = Product.objects.filter(is_featured=True)
        serializer = ProductSerializer(featured_products, many=True)
        return Response(serializer.data)

# View pour les produits en promotion
class PromotionProductsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        promotion_products = Product.objects.filter(promotion=True)
        serializer = ProductSerializer(promotion_products, many=True)
        return Response(serializer.data)

# View pour les produits sans promotion
class NosProduitsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        nos_produits = Product.objects.filter(promotion=False)
        serializer = ProductSerializer(nos_produits, many=True)
        return Response(serializer.data)

# Vue pour les produits du tableau de bord utilisateur
class DashboardProduits(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        username = kwargs.get('nom_cli')
        try:
            # Utilisation du modèle User personnalisé
            user = User.objects.get(nom_cli=username)
            produits = Product.objects.filter(user=user)
            serializer = ProductSerializer(produits, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Création d'un produit
class ProductCreateView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]  # ✅ Sécurisé - Admin seulement
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Mise à jour d'un produit
class ProductUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]  # ✅ Sécurisé - Admin seulement
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Suppression d'un produit
class ProductDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]  # ✅ Sécurisé - Admin seulement
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Vue pour les produits recommandés basés sur l'IA (similarité cosinus)
class RecommendedProductsView(APIView):
    """
    Retourne les produits recommandés pour un produit donné.
    Utilise un algorithme de similarité cosinus basé sur :
    - Catégorie
    - Marque
    - Prix
    - Spécifications techniques (RAM, stockage, écran)
    - Système d'exploitation
    - État du produit
    """
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            # Récupérer le produit cible
            target_product = get_object_or_404(Product, id=id)
            
            # Récupérer tous les autres produits disponibles (avec stock > 0)
            all_products = Product.objects.filter(stock__gt=0).exclude(id=id)
            
            # Obtenir les recommandations (limite à 10 par défaut)
            limit = int(request.query_params.get('limit', 10))
            recommended_products = get_recommended_products(
                target_product, 
                all_products, 
                limit=limit
            )
            
            # Sérialiser et retourner les résultats
            serializer = ProductSerializer(recommended_products, many=True)
            
            return Response({
                'count': len(recommended_products),
                'target_product_id': id,
                'recommendations': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response(
                {'error': 'Produit non trouvé'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': f'Erreur lors du calcul des recommandations: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
