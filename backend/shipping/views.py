from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ShippingAddress, ShippingZone
from .serializers import (
    ShippingAddressSerializer,
    ShippingAddressCreateSerializer,
    ShippingZoneSerializer,
)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les adresses de livraison.
    
    - GET /shipping/addresses/ : Liste des adresses de l'utilisateur
    - POST /shipping/addresses/ : Créer une nouvelle adresse
    - GET /shipping/addresses/{id}/ : Détails d'une adresse
    - PUT /shipping/addresses/{id}/ : Modifier une adresse
    - DELETE /shipping/addresses/{id}/ : Supprimer une adresse
    - POST /shipping/addresses/{id}/set_default/ : Définir comme adresse par défaut
    """
    serializer_class = ShippingAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ShippingAddressCreateSerializer
        return ShippingAddressSerializer

    def perform_create(self, serializer):
        # Si c'est la première adresse, la définir comme par défaut
        is_first = not ShippingAddress.objects.filter(user=self.request.user).exists()
        serializer.save(
            user=self.request.user,
            is_default=serializer.validated_data.get('is_default', is_first)
        )

    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Définir une adresse comme adresse par défaut"""
        address = self.get_object()
        
        # Retirer le défaut des autres adresses
        ShippingAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # Définir cette adresse comme par défaut
        address.is_default = True
        address.save()
        
        return Response({
            "message": "Adresse définie comme adresse par défaut",
            "address": ShippingAddressSerializer(address).data
        })

    @action(detail=False, methods=['get'])
    def default(self, request):
        """Récupérer l'adresse par défaut de l'utilisateur"""
        address = ShippingAddress.objects.filter(user=request.user, is_default=True).first()
        
        if not address:
            return Response(
                {"error": "Aucune adresse par défaut définie"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(ShippingAddressSerializer(address).data)


class ShippingZoneViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API pour récupérer les zones de livraison et leurs tarifs.
    
    - GET /shipping/zones/ : Liste des zones de livraison actives
    - GET /shipping/zones/{id}/ : Détails d'une zone
    - GET /shipping/zones/by_city/?city=Douala : Récupérer la zone par ville
    """
    serializer_class = ShippingZoneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return ShippingZone.objects.filter(is_active=True)

    @action(detail=False, methods=['get'])
    def by_city(self, request):
        """Récupérer les frais de livraison pour une ville donnée"""
        city = request.query_params.get('city', '').strip()
        
        if not city:
            return Response(
                {"error": "Le paramètre 'city' est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rechercher la zone correspondant à la ville (insensible à la casse)
        zone = ShippingZone.objects.filter(
            name__icontains=city,
            is_active=True
        ).first()
        
        if not zone:
            # Zone par défaut si la ville n'est pas trouvée
            default_zone = ShippingZone.objects.filter(
                name__icontains='autre',
                is_active=True
            ).first()
            
            if default_zone:
                return Response({
                    "zone": ShippingZoneSerializer(default_zone).data,
                    "message": f"Zone '{city}' non trouvée, tarif par défaut appliqué"
                })
            
            return Response(
                {"error": f"Aucune zone de livraison trouvée pour '{city}'"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(ShippingZoneSerializer(zone).data)
