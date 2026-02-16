import os
import sys
import django

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ['DATABASE_URL'] = "postgresql://e_commerce_6c64_user:kahJ0huW9mo8LnCPemTsRLTkdkXm7CGT@dpg-d69c0n0gjchc73chbnk0-a.oregon-postgres.render.com/e_commerce_6c64"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model
from backend.produits.models import Product, Brand
from backend.home.models import Banner, Category, Announcement

User = get_user_model()

print("=== Création des données de test ===\n")

# 1. Créer un superuser admin
print("1. Création de l'utilisateur admin...")
if not User.objects.filter(nom_cli='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        nom_cli='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("   ✓ Admin créé (login: admin / password: admin123)")
else:
    print("   - Admin existe déjà")

# 2. Créer un utilisateur test
print("2. Création de l'utilisateur test...")
if not User.objects.filter(nom_cli='testuser').exists():
    user = User.objects.create_user(
        username='testuser',
        nom_cli='testuser',
        email='test@example.com',
        password='test123',
        numero_cli='0123456789',
        adresse_cli='123 Rue Test',
        ville_cli='Paris',
        code_postal_cli='75001',
        pays_cli='France'
    )
    print("   ✓ Utilisateur test créé (login: testuser / password: test123)")
else:
    print("   - Utilisateur test existe déjà")

# 3. Créer les marques de téléphones
print("3. Création des marques...")
brands_names = ['Apple', 'Samsung', 'Xiaomi', 'Huawei', 'Google', 'OnePlus']

for brand_name in brands_names:
    brand, created = Brand.objects.get_or_create(name=brand_name)
    if created:
        print(f"   ✓ Marque créée: {brand.name}")

# 4. Créer les catégories
print("4. Création des catégories...")
categories_data = [
    {'name': 'Smartphones'},
    {'name': 'Accessoires'},
    {'name': 'Tablettes'},
    {'name': 'Montres connectées'},
]

for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name']
    )
    if created:
        print(f"   ✓ Catégorie créée: {cat.name}")

# 5. Créer les produits (téléphones)
print("5. Création des produits...")

# Récupérer l'admin pour l'associer aux produits
admin_user = User.objects.get(nom_cli='admin')
smartphones_cat = Category.objects.get(name='Smartphones')

products_data = [
    # Apple - Images GSMArena (courtes et fiables)
    {'name': 'iPhone 15 Pro Max', 'description': 'Le dernier iPhone avec puce A17 Pro, écran Super Retina XDR 6.7"', 'price': 1479, 'stock': 50, 'brand': 'Apple', 'ram': 8, 'storage': 256, 'screen_size': 6.7, 'battery_capacity': 4422, 'main_camera': '48 MP + 12 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15-pro-max.jpg'},
    {'name': 'iPhone 15', 'description': 'iPhone 15 avec Dynamic Island, puce A16 Bionic', 'price': 969, 'stock': 75, 'brand': 'Apple', 'ram': 6, 'storage': 128, 'screen_size': 6.1, 'battery_capacity': 3349, 'main_camera': '48 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-15.jpg'},
    {'name': 'iPhone 14', 'description': 'iPhone 14 avec écran Super Retina XDR, puce A15 Bionic', 'price': 769, 'stock': 100, 'brand': 'Apple', 'ram': 6, 'storage': 128, 'screen_size': 6.1, 'battery_capacity': 3279, 'main_camera': '12 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/apple-iphone-14.jpg'},
    # Samsung
    {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Galaxy S24 Ultra avec Galaxy AI, S Pen intégré', 'price': 1469, 'stock': 40, 'brand': 'Samsung', 'ram': 12, 'storage': 256, 'screen_size': 6.8, 'battery_capacity': 5000, 'main_camera': '200 MP + 12 MP + 50 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g.jpg'},
    {'name': 'Samsung Galaxy S24', 'description': 'Galaxy S24 avec écran Dynamic AMOLED 2X', 'price': 899, 'stock': 60, 'brand': 'Samsung', 'ram': 8, 'storage': 128, 'screen_size': 6.2, 'battery_capacity': 4000, 'main_camera': '50 MP + 12 MP + 10 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24.jpg'},
    {'name': 'Samsung Galaxy A54', 'description': 'Galaxy A54 5G avec écran Super AMOLED', 'price': 449, 'stock': 120, 'brand': 'Samsung', 'ram': 8, 'storage': 128, 'screen_size': 6.4, 'battery_capacity': 5000, 'main_camera': '50 MP + 12 MP + 5 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-a54-5g.jpg'},
    # Xiaomi
    {'name': 'Xiaomi 14 Ultra', 'description': 'Xiaomi 14 Ultra avec optique Leica, Snapdragon 8 Gen 3', 'price': 1299, 'stock': 35, 'brand': 'Xiaomi', 'ram': 16, 'storage': 512, 'screen_size': 6.73, 'battery_capacity': 5300, 'main_camera': '50 MP + 50 MP + 50 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-14-ultra.jpg'},
    {'name': 'Xiaomi Redmi Note 13 Pro', 'description': 'Redmi Note 13 Pro avec écran AMOLED, caméra 200 MP', 'price': 349, 'stock': 150, 'brand': 'Xiaomi', 'ram': 8, 'storage': 256, 'screen_size': 6.67, 'battery_capacity': 5100, 'main_camera': '200 MP + 8 MP + 2 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/xiaomi-redmi-note-13-pro-5g.jpg'},
    # Google
    {'name': 'Google Pixel 8 Pro', 'description': 'Pixel 8 Pro avec Tensor G3, 7 ans de mises à jour', 'price': 1099, 'stock': 45, 'brand': 'Google', 'ram': 12, 'storage': 128, 'screen_size': 6.7, 'battery_capacity': 5050, 'main_camera': '50 MP + 48 MP + 48 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8-pro.jpg'},
    {'name': 'Google Pixel 8', 'description': 'Pixel 8 avec puce Tensor G3, écran Actua', 'price': 799, 'stock': 55, 'brand': 'Google', 'ram': 8, 'storage': 128, 'screen_size': 6.2, 'battery_capacity': 4575, 'main_camera': '50 MP + 12 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/google-pixel-8.jpg'},
    # OnePlus
    {'name': 'OnePlus 12', 'description': 'OnePlus 12 avec Snapdragon 8 Gen 3, charge 100W', 'price': 919, 'stock': 40, 'brand': 'OnePlus', 'ram': 12, 'storage': 256, 'screen_size': 6.82, 'battery_capacity': 5400, 'main_camera': '50 MP + 48 MP + 64 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/oneplus-12.jpg'},
    # Huawei
    {'name': 'Huawei P60 Pro', 'description': 'Huawei P60 Pro avec optique XMAGE', 'price': 1099, 'stock': 30, 'brand': 'Huawei', 'ram': 8, 'storage': 256, 'screen_size': 6.67, 'battery_capacity': 4815, 'main_camera': '48 MP + 13 MP + 48 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://fdn2.gsmarena.com/vv/bigpic/huawei-p60-pro.jpg'},
]

for prod_data in products_data:
    product_name = prod_data['name']
    image_url = prod_data.pop('image_url', None)
    brand_name = prod_data.pop('brand')
    
    try:
        brand = Brand.objects.get(name=brand_name)
        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'brand': brand,
                'categorie': smartphones_cat,
                'user': admin_user,
                **prod_data
            }
        )
        
        # Mettre à jour l'image avec l'URL externe
        if image_url:
            product.image = image_url
            product.save()
        
        if created:
            print(f"   ✓ Produit créé: {product.name} - {product.price}€")
        else:
            print(f"   ✓ Image mise à jour: {product.name}")
    except Exception as e:
        print(f"   ✗ Erreur pour {product_name}: {e}")

# 6. Créer des bannières
print("6. Création des bannières...")
banners_data = [
    {'title': 'iPhone 15 Pro Max'},
    {'title': 'Samsung Galaxy S24'},
]

for banner_data in banners_data:
    banner, created = Banner.objects.get_or_create(title=banner_data['title'])
    if created:
        print(f"   ✓ Bannière créée: {banner.title}")

# 7. Créer les annonces défilantes
print("7. Création des annonces défilantes...")
announcements_data = [
    {'text': 'Livraison GRATUITE pour toute commande supérieure à 50 000 FCFA', 'emoji': '🔥', 'order': 1},
    {'text': 'Nouveaux iPhone 15 disponibles !', 'emoji': '📱', 'order': 2},
    {'text': 'Garantie 12 mois sur tous nos produits', 'emoji': '⚡', 'order': 3},
    {'text': 'Paiement sécurisé par Mobile Money et Carte Bancaire', 'emoji': '💳', 'order': 4},
    {'text': 'Service client disponible 24h/24 et 7j/7', 'emoji': '🎧', 'order': 5},
]

for ann_data in announcements_data:
    announcement, created = Announcement.objects.get_or_create(
        text=ann_data['text'],
        defaults={'emoji': ann_data['emoji'], 'order': ann_data['order'], 'is_active': True}
    )
    if created:
        print(f"   ✓ Annonce créée: {ann_data['emoji']} {ann_data['text'][:40]}...")

print("\n=== Données de test créées avec succès! ===")
print("\nComptes utilisateurs:")
print("  - Admin: admin / admin123")
print("  - Test:  testuser / test123")
print(f"\nProduits créés: {Product.objects.count()}")
print(f"Marques créées: {Brand.objects.count()}")
print(f"Catégories créées: {Category.objects.count()}")
print(f"Annonces créées: {Announcement.objects.filter(is_active=True).count()}")
