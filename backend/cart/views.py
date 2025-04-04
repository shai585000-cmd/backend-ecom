from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartView(APIView):
    def get(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemView(APIView):
    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        data = request.data
        item = CartItem.objects.create(
            cart=cart,
            product=data.get("product"),
            quantity=data.get("quantity", 1),
            price=data.get("price"),
        )
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get("pk")
        item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Exemple : Calcul du total
        total_price = sum(item.quantity * item.price for item in cart.items.all())
        # Logique pour traiter le paiement peut être ajoutée ici
        cart.items.all().delete()  # Vide le panier après paiement
        return Response({"message": "Checkout completed", "total_price": total_price})
