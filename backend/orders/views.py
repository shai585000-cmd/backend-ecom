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
from backend.produits.models import Product


class OrderViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les commandes.
    
    - GET /orders/ : Liste des commandes de l'utilisateur
    - POST /orders/ : Créer une commande à partir du panier
    - GET /orders/{id}/ : Détails d'une commande
    - POST /orders/{id}/cancel/ : Annuler une commande
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Retourne uniquement les commandes de l'utilisateur connecté"""
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).prefetch_related('items')
        return Order.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action == 'update_status':
            return OrderStatusUpdateSerializer
        return OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Créer une commande à partir des items envoyés depuis le frontend"""
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Récupérer les items du panier depuis la requête
        cart_items = serializer.validated_data.get('items', [])

        if not cart_items:
            return Response(
                {"error": "Votre panier est vide"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier le stock et récupérer les produits
        products_data = []
        for item in cart_items:
            try:
                product = Product.objects.get(id=item['product_id'])
                if product.stock < item['quantity']:
                    return Response(
                        {"error": f"Stock insuffisant pour {product.name}. Disponible: {product.stock}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                products_data.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': item['price']
                })
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Produit avec l'ID {item['product_id']} introuvable"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Calculer le total
        total_amount = sum(item['price'] * item['quantity'] for item in products_data)

        # Générer un numéro de commande unique
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        # Créer la commande (avec ou sans utilisateur connecté)
        order_data = {
            'order_number': order_number,
            'total_amount': total_amount,
            'shipping_address': serializer.validated_data['shipping_address'],
            'shipping_city': serializer.validated_data['shipping_city'],
            'shipping_phone': serializer.validated_data['shipping_phone'],
            'notes': serializer.validated_data.get('notes', ''),
        }
        
        # Si l'utilisateur est connecté, associer la commande à son compte
        if request.user.is_authenticated:
            order_data['user'] = request.user
        else:
            # Pour les commandes invités, stocker le nom et email si fournis
            order_data['guest_name'] = serializer.validated_data.get('guest_name', '')
            order_data['guest_email'] = serializer.validated_data.get('guest_email', '')
        
        order = Order.objects.create(**order_data)

        # Créer les articles de la commande et mettre à jour le stock
        for item in products_data:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                quantity=item['quantity'],
                unit_price=item['price'],
                total_price=item['price'] * item['quantity'],
            )
            # Décrémenter le stock
            product.stock -= item['quantity']
            product.save()

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
