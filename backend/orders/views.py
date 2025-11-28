import uuid
from django.db import transaction
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
)
from backend.cart.models import Cart, CartItem


class OrderViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les commandes.
    
    - GET /orders/ : Liste des commandes de l'utilisateur
    - POST /orders/ : Créer une commande à partir du panier
    - GET /orders/{id}/ : Détails d'une commande
    - POST /orders/{id}/cancel/ : Annuler une commande
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retourne uniquement les commandes de l'utilisateur connecté"""
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Créer une commande à partir du panier de l'utilisateur"""
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Récupérer le panier de l'utilisateur
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.select_related('product').all()
        except Cart.DoesNotExist:
            return Response(
                {"error": "Votre panier est vide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not cart_items.exists():
            return Response(
                {"error": "Votre panier est vide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier le stock de chaque produit
        for item in cart_items:
            if item.product and item.product.stock < item.quantity:
                return Response(
                    {"error": f"Stock insuffisant pour {item.product.name}. Disponible: {item.product.stock}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Calculer le total
        total_amount = sum(item.price * item.quantity for item in cart_items)

        # Générer un numéro de commande unique
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        # Créer la commande
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=total_amount,
            shipping_address=serializer.validated_data['shipping_address'],
            shipping_city=serializer.validated_data['shipping_city'],
            shipping_phone=serializer.validated_data['shipping_phone'],
            notes=serializer.validated_data.get('notes', ''),
        )

        # Créer les articles de la commande et mettre à jour le stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name if item.product else "Produit supprimé",
                quantity=item.quantity,
                unit_price=item.price,
                total_price=item.price * item.quantity,
            )
            # Décrémenter le stock
            if item.product:
                item.product.stock -= item.quantity
                item.product.save()

        # Vider le panier
        cart_items.delete()

        # Retourner la commande créée
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annuler une commande (seulement si elle est en attente)"""
        order = self.get_object()

        if order.status not in ['pending', 'confirmed']:
            return Response(
                {"error": "Cette commande ne peut plus être annulée"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Restaurer le stock
        for item in order.items.all():
            if item.product:
                item.product.stock += item.quantity
                item.product.save()

        order.status = 'cancelled'
        order.save()

        return Response(
            {"message": "Commande annulée avec succès"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """Mettre à jour le statut d'une commande (admin seulement)"""
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order.status = serializer.validated_data['status']
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )
