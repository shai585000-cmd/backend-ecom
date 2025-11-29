"""
Script pour créer les données de livraison.
Exécuter avec: python manage.py shell < create_shipping_data.py
Ou copier-coller dans le shell Django.
"""

from backend.shipping.models import ShippingZone

# Supprimer les anciennes zones si elles existent
ShippingZone.objects.all().delete()
print("Anciennes zones supprimées")

# Créer les zones de livraison
zones = [
    {'name': 'Abidjan', 'shipping_fee': 1500, 'estimated_days': 1, 'is_active': True},
    {'name': 'Douala', 'shipping_fee': 2000, 'estimated_days': 2, 'is_active': True},
    {'name': 'Yaoundé', 'shipping_fee': 2500, 'estimated_days': 3, 'is_active': True},
    {'name': 'Bouaké', 'shipping_fee': 2000, 'estimated_days': 2, 'is_active': True},
    {'name': 'San Pedro', 'shipping_fee': 2500, 'estimated_days': 3, 'is_active': True},
    {'name': 'Yamoussoukro', 'shipping_fee': 2000, 'estimated_days': 2, 'is_active': True},
    {'name': 'Autre', 'shipping_fee': 3000, 'estimated_days': 5, 'is_active': True},
]

for zone in zones:
    ShippingZone.objects.create(**zone)
    print(f"Zone créée: {zone['name']} - {zone['shipping_fee']} FCFA ({zone['estimated_days']} jour(s))")

print(f"\n✅ Total: {ShippingZone.objects.count()} zones créées")
