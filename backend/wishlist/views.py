from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist, WishlistItem
from backend.produits.models import Product
from backend.produits.serializers import ProductSerializer


class WishlistView(APIView):
    """Liste des produits dans la wishlist"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        items = wishlist.items.select_related('product')
        products = [item.product for item in items]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class WishlistAddView(APIView):
    """Ajouter un produit a la wishlist"""
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Produit non trouve"},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        
        if WishlistItem.objects.filter(wishlist=wishlist, product=product).exists():
            return Response(
                {"message": "Produit deja dans les favoris"},
                status=status.HTTP_200_OK
            )

        WishlistItem.objects.create(wishlist=wishlist, product=product)
        return Response(
            {"message": "Produit ajoute aux favoris"},
            status=status.HTTP_201_CREATED
        )


class WishlistRemoveView(APIView):
    """Retirer un produit de la wishlist"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if not wishlist:
            return Response(
                {"error": "Wishlist non trouvee"},
                status=status.HTTP_404_NOT_FOUND
            )

        deleted, _ = WishlistItem.objects.filter(
            wishlist=wishlist, 
            product_id=product_id
        ).delete()

        if deleted:
            return Response({"message": "Produit retire des favoris"})
        return Response(
            {"error": "Produit non trouve dans les favoris"},
            status=status.HTTP_404_NOT_FOUND
        )


class WishlistCheckView(APIView):
    """Verifier si un produit est dans la wishlist"""
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if not wishlist:
            return Response({"in_wishlist": False})

        in_wishlist = WishlistItem.objects.filter(
            wishlist=wishlist, 
            product_id=product_id
        ).exists()
        
        return Response({"in_wishlist": in_wishlist})
