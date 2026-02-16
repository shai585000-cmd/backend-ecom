import uuid
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from backend.orders.models import Order


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les paiements.
    
    - POST /payments/ : Créer un paiement pour une commande
    - GET /payments/ : Liste des paiements de l'utilisateur
    - GET /payments/{id}/ : Détails d'un paiement
    - POST /payments/{id}/confirm/ : Confirmer un paiement (Mobile Money)
    """
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Payment.objects.filter(user=self.request.user).select_related('order')
        return Payment.objects.none()

    def create(self, request, *args, **kwargs):
        """Créer un paiement pour une commande"""
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        payment_method = serializer.validated_data['payment_method']
        phone_number = serializer.validated_data.get('phone_number', '')

        # Vérifier que la commande existe
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(id=order_id, user=request.user)
            else:
                order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Commande introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier qu'il n'y a pas déjà un paiement pour cette commande
        if hasattr(order, 'payment'):
            return Response(
                {"error": "Un paiement existe déjà pour cette commande"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Générer un ID de transaction unique
        transaction_id = f"PAY-{uuid.uuid4().hex[:12].upper()}"

        # Créer le paiement (avec ou sans utilisateur)
        payment_data = {
            'order': order,
            'transaction_id': transaction_id,
            'payment_method': payment_method,
            'amount': order.total_amount,
            'phone_number': phone_number,
            'status': 'pending'
        }
        if request.user.is_authenticated:
            payment_data['user'] = request.user
        
        payment = Payment.objects.create(**payment_data)

        # Pour le paiement cash, on le marque comme "en attente de livraison"
        if payment_method == 'cash':
            payment.status = 'pending'
            payment.save()
            # Confirmer la commande
            order.status = 'confirmed'
            order.save()
            return Response({
                "message": "Commande confirmée. Paiement à la livraison.",
                "payment": PaymentSerializer(payment).data
            }, status=status.HTTP_201_CREATED)

        # Pour Mobile Money, on simule l'envoi d'une demande de paiement
        # En production, ici on appellerait l'API CinetPay ou autre
        if payment_method in ['mobile_money', 'orange_money']:
            # Simuler l'envoi d'une demande de paiement
            return Response({
                "message": f"Une demande de paiement a été envoyée au {phone_number}. Veuillez confirmer sur votre téléphone.",
                "payment": PaymentSerializer(payment).data,
                "instructions": self._get_payment_instructions(payment_method, phone_number, order.total_amount)
            }, status=status.HTTP_201_CREATED)

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )

    def _get_payment_instructions(self, method, phone, amount):
        """Retourne les instructions de paiement selon la méthode"""
        if method == 'orange_money':
            return {
                "steps": [
                    "1. Composez #144# sur votre téléphone",
                    "2. Sélectionnez 'Paiement marchand'",
                    f"3. Entrez le montant: {amount} FCFA",
                    "4. Confirmez avec votre code secret",
                    "5. Vous recevrez un SMS de confirmation"
                ],
                "merchant_code": "VOTRE_CODE_MARCHAND"  # À configurer
            }
        elif method == 'mobile_money':
            return {
                "steps": [
                    "1. Composez *133# sur votre téléphone",
                    "2. Sélectionnez 'Paiement'",
                    f"3. Entrez le montant: {amount} FCFA",
                    "4. Confirmez avec votre code PIN",
                    "5. Vous recevrez un SMS de confirmation"
                ],
                "merchant_code": "VOTRE_CODE_MARCHAND"  # À configurer
            }
        return {}

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """
        Confirmer manuellement un paiement Mobile Money.
        En production, ceci serait appelé par un webhook de CinetPay.
        """
        payment = self.get_object()

        if payment.status == 'completed':
            return Response(
                {"error": "Ce paiement est déjà confirmé"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Marquer le paiement comme complété
        payment.status = 'completed'
        payment.save()

        # Confirmer la commande
        payment.order.status = 'confirmed'
        payment.order.save()

        return Response({
            "message": "Paiement confirmé avec succès",
            "payment": PaymentSerializer(payment).data
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annuler un paiement en attente"""
        payment = self.get_object()

        if payment.status != 'pending':
            return Response(
                {"error": "Seuls les paiements en attente peuvent être annulés"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payment.status = 'failed'
        payment.save()

        return Response({
            "message": "Paiement annulé",
            "payment": PaymentSerializer(payment).data
        })
