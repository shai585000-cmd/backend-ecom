"""
Script pour remplir la base de donnees avec des donnees de test.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from backend.produits.models import Product
from backend.home.models import Category, Banner
from backend.shipping.models import ShippingZone

User = get_user_model()

print("=" * 50)
print("REMPLISSAGE DE LA BASE DE DONNEES")
print("=" * 50)

# ============================================
# 1. CATEGORIES
# ============================================
print("\n[1/5] Creation des categories...")

categories_data = [
    {'name': 'Smartphones', 'description': 'Telephones portables derniere generation'},
    {'name': 'Accessoires', 'description': 'Coques, chargeurs, ecouteurs et plus'},
    {'name': 'Tablettes', 'description': 'Tablettes tactiles pour tous usages'},
    {'name': 'Montres Connectees', 'description': 'Smartwatches et bracelets connectes'},
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories[cat_data['name']] = cat
    status = "Cree" if created else "Existe deja"
    print(f"  - {cat.name}: {status}")

# Creer un utilisateur vendeur pour les produits
print("\n[1.5/5] Creation utilisateur vendeur...")
vendeur, created = User.objects.get_or_create(
    username='vendeur',
    defaults={
        'email': 'vendeur@ivoiremarket.com',
        'first_name': 'Vendeur',
        'last_name': 'Principal'
    }
)
if created:
    vendeur.set_password('Vendeur123!')
    vendeur.save()
    print(f"  - Vendeur cree: vendeur / Vendeur123!")
else:
    print(f"  - Vendeur existe deja")

# ============================================
# 2. PRODUITS (TELEPHONES)
# ============================================
print("\n[2/5] Creation des produits...")

products_data = [
    # SMARTPHONES
    {
        'name': 'iPhone 15 Pro Max',
        'title': 'iPhone 15 Pro Max 256GB',
        'description': 'Le dernier iPhone avec puce A17 Pro, camera 48MP, ecran Super Retina XDR 6.7 pouces. Titane naturel.',
        'price': 850000,
        'stock': 5,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600',
        'promotion': False
    },
    {
        'name': 'iPhone 15',
        'title': 'iPhone 15 128GB',
        'description': 'iPhone 15 avec Dynamic Island, camera 48MP, puce A16 Bionic. Design en aluminium.',
        'price': 650000,
        'stock': 8,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1696446701796-da61225697cc?w=600',
        'promotion': True
    },
    {
        'name': 'Samsung Galaxy S24 Ultra',
        'title': 'Samsung Galaxy S24 Ultra 256GB',
        'description': 'Le meilleur Samsung avec S Pen integre, camera 200MP, ecran AMOLED 6.8 pouces, Galaxy AI.',
        'price': 800000,
        'stock': 6,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=600',
        'promotion': False
    },
    {
        'name': 'Samsung Galaxy A54',
        'title': 'Samsung Galaxy A54 5G 128GB',
        'description': 'Excellent rapport qualite-prix. Ecran Super AMOLED 6.4", camera 50MP, batterie 5000mAh.',
        'price': 280000,
        'stock': 15,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=600',
        'promotion': True
    },
    {
        'name': 'Samsung Galaxy A14',
        'title': 'Samsung Galaxy A14 64GB',
        'description': 'Smartphone abordable avec ecran 6.6", triple camera, batterie longue duree.',
        'price': 120000,
        'stock': 20,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600',
        'promotion': False
    },
    {
        'name': 'Xiaomi Redmi Note 13 Pro',
        'title': 'Xiaomi Redmi Note 13 Pro 256GB',
        'description': 'Camera 200MP, ecran AMOLED 120Hz, charge rapide 67W. Le best-seller Xiaomi.',
        'price': 200000,
        'stock': 12,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=600',
        'promotion': False
    },
    {
        'name': 'Xiaomi Poco X6 Pro',
        'title': 'Xiaomi Poco X6 Pro 5G 256GB',
        'description': 'Performance gaming avec Dimensity 8300, ecran 120Hz, charge 67W.',
        'price': 250000,
        'stock': 10,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600',
        'promotion': True
    },
    {
        'name': 'OPPO Reno 11',
        'title': 'OPPO Reno 11 5G 256GB',
        'description': 'Design elegant, camera portrait professionnelle, charge SUPERVOOC 67W.',
        'price': 320000,
        'stock': 7,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1592899677977-9c10ca588bbd?w=600',
        'promotion': False
    },
    {
        'name': 'Tecno Camon 20 Pro',
        'title': 'Tecno Camon 20 Pro 256GB',
        'description': 'Le roi des selfies avec camera frontale 32MP, ecran AMOLED, design premium.',
        'price': 180000,
        'stock': 14,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1605236453806-6ff36851218e?w=600',
        'promotion': False
    },
    {
        'name': 'Infinix Note 40 Pro',
        'title': 'Infinix Note 40 Pro 256GB',
        'description': 'Charge sans fil magnetique, ecran 3D curved AMOLED, camera 108MP.',
        'price': 220000,
        'stock': 9,
        'category': 'Smartphones',
        'image': 'https://images.unsplash.com/photo-1512054502232-10a0a035d672?w=600',
        'promotion': True
    },
    
    # ACCESSOIRES
    {
        'name': 'AirPods Pro 2',
        'title': 'Apple AirPods Pro 2eme generation',
        'description': 'Reduction de bruit active, audio spatial, boitier MagSafe USB-C.',
        'price': 180000,
        'stock': 12,
        'category': 'Accessoires',
        'image': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=600',
        'promotion': False
    },
    {
        'name': 'Samsung Galaxy Buds 2 Pro',
        'title': 'Samsung Galaxy Buds2 Pro',
        'description': 'Son Hi-Fi 24bit, ANC intelligent, confort toute la journee.',
        'price': 120000,
        'stock': 15,
        'category': 'Accessoires',
        'image': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600',
        'promotion': True
    },
    {
        'name': 'Chargeur Rapide 65W',
        'title': 'Chargeur USB-C 65W GaN',
        'description': 'Chargeur compact GaN, compatible tous smartphones, charge rapide.',
        'price': 25000,
        'stock': 30,
        'category': 'Accessoires',
        'image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600',
        'promotion': False
    },
    {
        'name': 'Coque iPhone 15 Pro',
        'title': 'Coque MagSafe iPhone 15 Pro',
        'description': 'Protection premium, compatible MagSafe, plusieurs coloris disponibles.',
        'price': 15000,
        'stock': 50,
        'category': 'Accessoires',
        'image': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600',
        'promotion': False
    },
    {
        'name': 'Power Bank 20000mAh',
        'title': 'Batterie Externe 20000mAh',
        'description': 'Charge rapide 22.5W, 2 ports USB + 1 USB-C, affichage LED.',
        'price': 35000,
        'stock': 25,
        'category': 'Accessoires',
        'image': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600',
        'promotion': True
    },
    
    # TABLETTES
    {
        'name': 'iPad Air M2',
        'title': 'Apple iPad Air M2 256GB',
        'description': 'Puce M2 ultra rapide, ecran Liquid Retina 10.9", compatible Apple Pencil Pro.',
        'price': 500000,
        'stock': 4,
        'category': 'Tablettes',
        'image': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600',
        'promotion': False
    },
    {
        'name': 'Samsung Galaxy Tab S9',
        'title': 'Samsung Galaxy Tab S9 128GB',
        'description': 'Ecran AMOLED 11", S Pen inclus, etanche IP68, DeX mode.',
        'price': 450000,
        'stock': 5,
        'category': 'Tablettes',
        'image': 'https://images.unsplash.com/photo-1561154464-82e9adf32764?w=600',
        'promotion': False
    },
    
    # MONTRES
    {
        'name': 'Apple Watch Series 9',
        'title': 'Apple Watch Series 9 45mm GPS',
        'description': 'Puce S9, Double Tap, ecran Retina always-on, suivi sante avance.',
        'price': 350000,
        'stock': 6,
        'category': 'Montres Connectees',
        'image': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=600',
        'promotion': False
    },
    {
        'name': 'Samsung Galaxy Watch 6',
        'title': 'Samsung Galaxy Watch 6 44mm',
        'description': 'Suivi sommeil, ECG, composition corporelle, Android et iOS.',
        'price': 250000,
        'stock': 8,
        'category': 'Montres Connectees',
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600',
        'promotion': True
    },
]

for prod_data in products_data:
    category = categories.get(prod_data['category'])
    if not category:
        print(f"  - ERREUR: Categorie '{prod_data['category']}' non trouvee")
        continue
    
    product, created = Product.objects.get_or_create(
        name=prod_data['name'],
        defaults={
            'description': prod_data['description'],
            'price': prod_data['price'],
            'stock': prod_data['stock'],
            'categorie': category,
            'image': prod_data['image'],
            'promotion': prod_data.get('promotion', False),
            'user': vendeur
        }
    )
    status = "Cree" if created else "Existe deja"
    print(f"  - {product.name}: {status}")

# ============================================
# 3. ZONES DE LIVRAISON
# ============================================
print("\n[3/5] Creation des zones de livraison...")

zones_data = [
    {'name': 'Abidjan', 'shipping_fee': 1500, 'estimated_days': 1, 'is_active': True},
    {'name': 'Yamoussoukro', 'shipping_fee': 2500, 'estimated_days': 2, 'is_active': True},
    {'name': 'Bouake', 'shipping_fee': 2500, 'estimated_days': 2, 'is_active': True},
    {'name': 'San Pedro', 'shipping_fee': 3000, 'estimated_days': 3, 'is_active': True},
    {'name': 'Korhogo', 'shipping_fee': 3500, 'estimated_days': 3, 'is_active': True},
    {'name': 'Daloa', 'shipping_fee': 3000, 'estimated_days': 2, 'is_active': True},
    {'name': 'Man', 'shipping_fee': 3500, 'estimated_days': 3, 'is_active': True},
    {'name': 'Douala', 'shipping_fee': 5000, 'estimated_days': 5, 'is_active': True},
    {'name': 'Yaounde', 'shipping_fee': 5500, 'estimated_days': 5, 'is_active': True},
    {'name': 'Autre', 'shipping_fee': 4000, 'estimated_days': 5, 'is_active': True},
]

for zone_data in zones_data:
    zone, created = ShippingZone.objects.get_or_create(
        name=zone_data['name'],
        defaults={
            'shipping_fee': zone_data['shipping_fee'],
            'estimated_days': zone_data['estimated_days'],
            'is_active': zone_data['is_active']
        }
    )
    status = "Cree" if created else "Existe deja"
    print(f"  - {zone.name}: {zone.shipping_fee} FCFA ({status})")

# ============================================
# 4. BANNERS ACCUEIL
# ============================================
print("\n[4/5] Creation des banners...")

banners_data = [
    {'title': 'iPhone 15 Pro Max', 'link': '/produit'},
    {'title': 'Samsung Galaxy S24', 'link': '/produit'},
    {'title': 'Accessoires Premium', 'link': '/produit'},
]

for banner_data in banners_data:
    banner, created = Banner.objects.get_or_create(
        title=banner_data['title'],
        defaults={'link': banner_data['link']}
    )
    status = "Cree" if created else "Existe deja"
    print(f"  - {banner.title}: {status}")

# ============================================
# 5. UTILISATEUR TEST
# ============================================
print("\n[5/5] Creation utilisateur test...")

test_user, created = User.objects.get_or_create(
    username='client_test',
    defaults={
        'email': 'client@test.com',
        'first_name': 'Client',
        'last_name': 'Test'
    }
)
if created:
    test_user.set_password('Test1234!')
    test_user.save()
    print(f"  - Utilisateur cree: client_test / Test1234!")
else:
    print(f"  - Utilisateur existe deja: client_test")

# ============================================
# RESUME
# ============================================
print("\n" + "=" * 50)
print("RESUME")
print("=" * 50)
print(f"Categories: {Category.objects.count()}")
print(f"Produits: {Product.objects.count()}")
print(f"Zones livraison: {ShippingZone.objects.count()}")
print(f"Banners: {Banner.objects.count()}")
print(f"Utilisateurs: {User.objects.count()}")
print("\nBase de donnees remplie avec succes!")
