import os
import sys
import django

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ['DATABASE_URL'] = "postgresql://postgres.uluantlvcdxnphaartlz:Offoange%4019@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model
from backend.produits.models import Product, Brand
from backend.home.models import Banner, Category, Announcement, HeroSection, FeatureItem, SolutionCard

User = get_user_model()

print("=== Création des données de test ===\n")

# 1. Créer un superuser admin
print("1. Création de l'utilisateur admin...")
if not User.objects.filter(nom_cli='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        nom_cli='admin',
        email='admin@example.com',
        password='admin123',
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

# 3. Créer les marques de téléphones et ordinateurs
print("3. Création des marques...")
brands_names = ['Apple', 'Samsung', 'Xiaomi', 'Huawei', 'Google', 'OnePlus', 'HP', 'Dell', 'Lenovo', 'Asus', 'MSI', 'Acer']

for brand_name in brands_names:
    brand, created = Brand.objects.get_or_create(name=brand_name)
    if created:
        print(f"   ✓ Marque créée: {brand.name}")

# 4. Créer les catégories
print("4. Création des catégories...")
categories_data = [
    {'name': 'Smartphones'},
    {'name': 'Accessoires'},
    {'name': 'Ordinateurs'},
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
    {'name': 'iPhone 15 Pro Max', 'description': 'Le dernier iPhone avec puce A17 Pro, écran Super Retina XDR 6.7"', 'price': 1479, 'stock': 50, 'brand': 'Apple', 'ram': 8, 'storage': 256, 'screen_size': 6.7, 'battery_capacity': 4422, 'main_camera': '48 MP + 12 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1771243522/media/products/0195949018930_h_f_l_2_r5vwtb.jpg'},
    {'name': 'iPhone 15', 'description': 'iPhone 15 avec Dynamic Island, puce A16 Bionic', 'price': 969, 'stock': 75, 'brand': 'Apple', 'ram': 6, 'storage': 128, 'screen_size': 6.1, 'battery_capacity': 3349, 'main_camera': '48 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776214442/media/products/0195949036781_h_f_l_0_c8pzqm.webp'},
    {'name': 'iPhone 14', 'description': 'iPhone 14 avec écran Super Retina XDR, puce A15 Bionic', 'price': 769, 'stock': 100, 'brand': 'Apple', 'ram': 6, 'storage': 128, 'screen_size': 6.1, 'battery_capacity': 3279, 'main_camera': '12 MP + 12 MP', 'operating_system': 'ios', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1771243471/media/products/apple-iphone-14-128-go-bleu_b4d01954-eecf-46e6-8838-eacfaa513062_o371sy.webp'},
    # Samsung
    {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Galaxy S24 Ultra avec Galaxy AI, S Pen intégré', 'price': 1469, 'stock': 40, 'brand': 'Samsung', 'ram': 12, 'storage': 256, 'screen_size': 6.8, 'battery_capacity': 5000, 'main_camera': '200 MP + 12 MP + 50 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776388198/media/products/samsung-galaxy-s24-ultra-1_pyv6gs.jpg'},
    {'name': 'Samsung Galaxy S24', 'description': 'Galaxy S24 avec écran Dynamic AMOLED 2X', 'price': 899, 'stock': 60, 'brand': 'Samsung', 'ram': 8, 'storage': 128, 'screen_size': 6.2, 'battery_capacity': 4000, 'main_camera': '50 MP + 12 MP + 10 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776388223/media/products/samsung-s24-5g-8gb-ram-256gb-_dkpypq.jpg'},
    {'name': 'Samsung Galaxy A54', 'description': 'Galaxy A54 5G avec écran Super AMOLED', 'price': 449, 'stock': 120, 'brand': 'Samsung', 'ram': 8, 'storage': 128, 'screen_size': 6.4, 'battery_capacity': 5000, 'main_camera': '50 MP + 12 MP + 5 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776388313/media/products/samsung-galaxy-a54-8gb-ram-128gb-5g_a5ct8d.jpg'},
    # Xiaomi
    {'name': 'Xiaomi 14 Ultra', 'description': 'Xiaomi 14 Ultra avec optique Leica, Snapdragon 8 Gen 3', 'price': 1299, 'stock': 35, 'brand': 'Xiaomi', 'ram': 16, 'storage': 512, 'screen_size': 6.73, 'battery_capacity': 5300, 'main_camera': '50 MP + 50 MP + 50 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776388282/media/products/xiaomi-14-ultra-16gb-ram-512gb-2_mbzc4t.jpg'},
    {'name': 'Xiaomi Redmi Note 13 Pro', 'description': 'Redmi Note 13 Pro avec écran AMOLED, caméra 200 MP', 'price': 349, 'stock': 150, 'brand': 'Xiaomi', 'ram': 8, 'storage': 256, 'screen_size': 6.67, 'battery_capacity': 5100, 'main_camera': '200 MP + 8 MP + 2 MP', 'operating_system': 'android', 'network': '5g', 'image_url': ''},
    # Google
    {'name': 'Google Pixel 8 Pro', 'description': 'Pixel 8 Pro avec Tensor G3, 7 ans de mises à jour', 'price': 1099, 'stock': 45, 'brand': 'Google', 'ram': 12, 'storage': 128, 'screen_size': 6.7, 'battery_capacity': 5050, 'main_camera': '50 MP + 48 MP + 48 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776387475/media/products/14102_i0iivt.jpg'},
    {'name': 'Google Pixel 8', 'description': 'Pixel 8 avec puce Tensor G3, écran Actua', 'price': 799, 'stock': 55, 'brand': 'Google', 'ram': 8, 'storage': 128, 'screen_size': 6.2, 'battery_capacity': 4575, 'main_camera': '50 MP + 12 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776387520/media/products/google-pixel-8-128gb-3_fovidf.jpg'},
    # OnePlus
    {'name': 'OnePlus 12', 'description': 'OnePlus 12 avec Snapdragon 8 Gen 3, charge 100W', 'price': 919, 'stock': 40, 'brand': 'OnePlus', 'ram': 12, 'storage': 256, 'screen_size': 6.82, 'battery_capacity': 5400, 'main_camera': '50 MP + 48 MP + 64 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776387652/media/products/oneplus-12-5g-12gb-ram-512gb_uvrgdk.jpg'},
    # Huawei
    {'name': 'Huawei P60 Pro', 'description': 'Huawei P60 Pro avec optique XMAGE', 'price': 1099, 'stock': 30, 'brand': 'Huawei', 'ram': 8, 'storage': 256, 'screen_size': 6.67, 'battery_capacity': 4815, 'main_camera': '48 MP + 13 MP + 48 MP', 'operating_system': 'android', 'network': '5g', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776387686/media/products/huawei-p60-pro-12gb-512gb-noir_3_800x_ze8hxw.webp'},
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

# 6. Créer les produits accessoires (Tech Accessories)
print("6. Création des produits accessoires...")

accessories_cat = Category.objects.get(name='Accessoires')

accessories_data = [
    # Étuis de protection
    {'name': 'Étui iPhone 15 Pro Max - Silicone Noir', 'description': 'Étui en silicone Apple avec boutons tactiles, protection MagSafe', 'price': 59, 'stock': 200, 'brand': 'Apple', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520522/media/products/1_1_aytxd5.jpg'},
    {'name': 'Étui iPhone 15 - Clear Transparent', 'description': 'Étui transparent ultra-fin, protection anti-rayures', 'price': 39, 'stock': 180, 'brand': 'Apple', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520468/media/products/MT213_xb0juj.jpg'},
    {'name': 'Étui Samsung Galaxy S24 Ultra - Noir', 'description': 'Étui officiel Samsung avec support intégré, protection renforcée', 'price': 49, 'stock': 150, 'brand': 'Samsung', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520219/media/products/images_5_jrzxgj.jpg'},
    {'name': 'Étui Samsung Galaxy S24 - Bleu Marine', 'description': 'Étui Slim Fit, protection légère et élégante', 'price': 35, 'stock': 160, 'brand': 'Samsung', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520420/media/products/Coque-silicone-noir-Samsung-S24_rmpmv3.jpg'},
    # Chargeurs
    {'name': 'Chargeur Rapide Apple 20W USB-C', 'description': 'Chargeur rapide officiel Apple, compatible iPhone et iPad', 'price': 29, 'stock': 250, 'brand': 'Apple', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776519113/media/products/sec-vrak-c20w-dv2-3_zhep5g.jpg'},
    {'name': 'Chargeur Samsung 45W Super Fast Charging', 'description': 'Chargeur rapide 45W avec USB-C, compatible Galaxy S series', 'price': 39, 'stock': 200, 'brand': 'Samsung', 'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520098/media/products/pack-sam-bk-epta845-r_i38hgy.jpg'},
    {'name': 'Chargeur Anker 20W PIQ 3.0 USB-C', 'description': 'Chargeur compact avec technologie PowerIQ, compatible tous appareils', 'price': 25, 'stock': 300, 'brand': 'Anker', 'image_url': ''},
    {'name': 'Chargeur Rapide 65W GaN USB-C', 'description': 'Chargeur compact GaN, compatible laptops et smartphones', 'price': 49, 'stock': 150, 'brand': 'Anker', 'image_url': ''},
    # Câbles
    {'name': 'Câble Lightning vers USB-C Apple 1m', 'description': 'Câble officiel Apple pour charge et synchronisation', 'price': 25, 'stock': 280, 'brand': 'Apple', 'image_url': ''},
    {'name': 'Câble USB-C vers USB-C Samsung 1.5m', 'description': 'Câble Samsung pour charge rapide et transfert de données', 'price': 19, 'stock': 320, 'brand': 'Samsung', 'image_url': ''},
    {'name': 'Câble USB-C vers Lightning Anker PowerLine II 2m', 'description': 'Câble renforcé MFi, garantie 18 mois', 'price': 22, 'stock': 250, 'brand': 'Anker', 'image_url': ''},
    # Écouteurs
    {'name': 'AirPods Pro 2ème génération avec MagSafe', 'description': 'Écouteurs Bluetooth avec réduction de bruit active, étui MagSafe', 'price': 279, 'stock': 100, 'brand': 'Apple', 'image_url': ''},
    {'name': 'AirPods 3ème génération', 'description': 'Écouteurs Bluetooth avec son spatial, étui MagSafe', 'price': 189, 'stock': 120, 'brand': 'Apple', 'image_url': ''},
    {'name': 'Samsung Galaxy Buds2 Pro', 'description': 'Écouteurs Bluetooth avec réduction de bruit active, son 360°', 'price': 229, 'stock': 110, 'brand': 'Samsung', 'image_url': ''},
    {'name': 'Samsung Galaxy Buds2', 'description': 'Écouteurs Bluetooth légers avec réduction de bruit active', 'price': 149, 'stock': 130, 'brand': 'Samsung', 'image_url': ''},
    {'name': 'Écouteurs Anker Soundcore Liberty 4 NC', 'description': 'Écouteurs Bluetooth avec réduction de bruit adaptative, 50h autonomie', 'price': 99, 'stock': 200, 'brand': 'Anker', 'image_url': ''},
    {'name': 'Écouteurs JBL Tune 225TWS', 'description': 'Écouteurs Bluetooth JBL Pure Bass, 40h autonomie', 'price': 89, 'stock': 180, 'brand': 'JBL', 'image_url': ''},
    # Batteries externes
    {'name': 'Batterie externe Anker PowerCore 10000', 'description': 'Batterie portable 10000mAh compacte, charge rapide PowerIQ', 'price': 39, 'stock': 150, 'brand': 'Anker', 'image_url': ''},
    {'name': 'Batterie externe Samsung 10000mAh', 'description': 'Batterie portable Samsung avec charge rapide 25W', 'price': 45, 'stock': 140, 'brand': 'Samsung', 'image_url': ''},
    {'name': 'Batterie externe Anker PowerCore 20000', 'description': 'Batterie portable 20000mAh, double USB, charge rapide', 'price': 59, 'stock': 120, 'brand': 'Anker', 'image_url': ''},
    # Adaptateurs
    {'name': 'Adaptateur USB-C vers HDMI Apple', 'description': 'Adaptateur officiel Apple pour connecter écrans externes', 'price': 69, 'stock': 80, 'brand': 'Apple', 'image_url': ''},
    {'name': 'Adaptateur Samsung USB-C Multiport', 'description': 'Adaptateur Samsung avec HDMI, USB 3.0 et USB-C', 'price': 55, 'stock': 90, 'brand': 'Samsung', 'image_url': ''},
    # Verres protecteurs
    {'name': 'Verre trempé iPhone 15 Pro Max - Pack de 3', 'description': 'Verres protecteurs ultra-fins avec protection antibactérienne', 'price': 29, 'stock': 300, 'brand': 'Apple', 'image_url': ''},
    {'name': 'Verre trempé Samsung Galaxy S24 Ultra - Pack de 2', 'description': 'Verres protecteurs Samsung avec protection écran complète', 'price': 24, 'stock': 280, 'brand': 'Samsung', 'image_url': ''},
]

for prod_data in accessories_data:
    product_name = prod_data['name']
    image_url = prod_data.pop('image_url', None)
    brand_name = prod_data.pop('brand')
    
    try:
        brand, _ = Brand.objects.get_or_create(name=brand_name)
        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'brand': brand,
                'categorie': accessories_cat,
                'user': admin_user,
                **prod_data
            }
        )
        
        if image_url:
            product.image = image_url
            product.save()
        
        if created:
            print(f"   ✓ Accessoire créé: {product.name} - {product.price}€")
        else:
            print(f"   - Accessoire existe déjà: {product.name}")
    except Exception as e:
        print(f"   ✗ Erreur pour {product_name}: {e}")

# 7. Créer les produits ordinateurs
print("7. Création des produits ordinateurs...")

computers_cat = Category.objects.get(name='Ordinateurs')

computers_data = [
    # MacBooks
    {
        'name': 'MacBook Pro 14" M3 Pro',
        'description': 'Puce M3 Pro, 18 Go RAM, 512 Go SSD, écran Liquid Retina XDR',
        'price': 2499,
        'stock': 25,
        'brand': 'Apple',
        'ram': 18,
        'storage': 512,
        'screen_size': 14.2,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520634/media/products/macbook-pro-m3-14-space-gray_1_r1kx5c.jpg',
    },
    {
        'name': 'MacBook Air 15" M3',
        'description': 'Puce M3, 8 Go RAM, 256 Go SSD, écran Liquid Retina',
        'price': 1499,
        'stock': 40,
        'brand': 'Apple',
        'ram': 8,
        'storage': 256,
        'screen_size': 15.3,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520682/media/products/macbook-air-m3-15-midnight_1_1_1_c1h9jv.jpg',
    },
    {
        'name': 'MacBook Air 13" M2',
        'description': 'Puce M2, 8 Go RAM, 256 Go SSD, design ultra-fin',
        'price': 1199,
        'stock': 50,
        'brand': 'Apple',
        'ram': 8,
        'storage': 256,
        'screen_size': 13.6,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520725/media/products/macbook-air-m2-13-midnight.jpg',
    },
    # HP
    {
        'name': 'HP Pavilion 15',
        'description': 'Intel Core i5, 8 Go RAM, 512 Go SSD, Windows 11',
        'price': 699,
        'stock': 60,
        'brand': 'HP',
        'ram': 8,
        'storage': 512,
        'screen_size': 15.6,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520778/media/products/hp-pavilion-15.jpg',
    },
    {
        'name': 'HP Spectre x360 14',
        'description': 'Intel Core i7, 16 Go RAM, 1 To SSD, écran OLED tactile',
        'price': 1599,
        'stock': 20,
        'brand': 'HP',
        'ram': 16,
        'storage': 1000,
        'screen_size': 14.0,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520812/media/products/hp-spectre-x360-14.jpg',
    },
    # Dell
    {
        'name': 'Dell XPS 15',
        'description': 'Intel Core i7, 16 Go RAM, 512 Go SSD, écran 3.5K OLED',
        'price': 1799,
        'stock': 30,
        'brand': 'Dell',
        'ram': 16,
        'storage': 512,
        'screen_size': 15.6,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520856/media/products/dell-xps-15.jpg',
    },
    {
        'name': 'Dell Inspiron 14',
        'description': 'Intel Core i5, 8 Go RAM, 256 Go SSD, Windows 11',
        'price': 599,
        'stock': 70,
        'brand': 'Dell',
        'ram': 8,
        'storage': 256,
        'screen_size': 14.0,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520890/media/products/dell-inspiron-14.jpg',
    },
    # Lenovo
    {
        'name': 'Lenovo ThinkPad X1 Carbon',
        'description': 'Intel Core i7, 16 Go RAM, 512 Go SSD, écran 14" 2.8K',
        'price': 1899,
        'stock': 25,
        'brand': 'Lenovo',
        'ram': 16,
        'storage': 512,
        'screen_size': 14.0,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520934/media/products/lenovo-thinkpad-x1-carbon.jpg',
    },
    {
        'name': 'Lenovo IdeaPad Slim 5',
        'description': 'AMD Ryzen 7, 16 Go RAM, 512 Go SSD, écran 16" 2.5K',
        'price': 899,
        'stock': 45,
        'brand': 'Lenovo',
        'ram': 16,
        'storage': 512,
        'screen_size': 16.0,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776520978/media/products/lenovo-ideapad-slim-5.jpg',
    },
    # Gaming
    {
        'name': 'Asus ROG Strix G16',
        'description': 'Intel Core i9, RTX 4070, 16 Go RAM, 1 To SSD, 165Hz',
        'price': 1999,
        'stock': 15,
        'brand': 'Asus',
        'ram': 16,
        'storage': 1000,
        'screen_size': 16.0,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776521022/media/products/asus-rog-strix-g16.jpg',
    },
    {
        'name': 'MSI Katana 15',
        'description': 'Intel Core i7, RTX 4060, 16 Go RAM, 512 Go SSD, 144Hz',
        'price': 1299,
        'stock': 20,
        'brand': 'MSI',
        'ram': 16,
        'storage': 512,
        'screen_size': 15.6,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776521066/media/products/msi-katana-15.jpg',
    },
    {
        'name': 'Acer Nitro 5',
        'description': 'AMD Ryzen 5, RTX 3050, 8 Go RAM, 512 Go SSD, 144Hz',
        'price': 799,
        'stock': 35,
        'brand': 'Acer',
        'ram': 8,
        'storage': 512,
        'screen_size': 15.6,
        'image_url': 'https://res.cloudinary.com/dirmdexmb/image/upload/v1776521110/media/products/acer-nitro-5.jpg',
    },
]

for prod_data in computers_data:
    product_name = prod_data['name']
    image_url = prod_data.pop('image_url', None)
    brand_name = prod_data.pop('brand')

    try:
        brand = Brand.objects.get(name=brand_name)
        product, created = Product.objects.get_or_create(
            name=product_name,
            defaults={
                'brand': brand,
                'categorie': computers_cat,
                'user': admin_user,
                'condition': 'new',
                **prod_data
            }
        )

        if image_url:
            product.image = image_url
            product.save()

        if created:
            print(f"   ✓ Ordinateur créé: {product.name} - {product.price}€")
        else:
            print(f"   ✓ Image mise à jour: {product.name}")
    except Exception as e:
        print(f"   ✗ Erreur pour {product_name}: {e}")

# 8. Créer des bannières
print("8. Création des bannières...")
banners_data = [
    {'title': 'iPhone 15 Pro Max'},
    {'title': 'Samsung Galaxy S24'},
]

for banner_data in banners_data:
    banner, created = Banner.objects.get_or_create(title=banner_data['title'])
    if created:
        print(f"   ✓ Bannière créée: {banner.title}")

# 9. Créer les annonces défilantes
print("9. Création des annonces défilantes...")
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

# 10. Créer la section Hero
print("10. Création de la section Hero...")
hero, created = HeroSection.objects.get_or_create(
    id=1,
    defaults={
        'badge_text': 'New 2024',
        'title': 'Discover the best smartphones on the market',
        'title_highlight': 'smartphones',
        'description': 'iPhone 15, Samsung Galaxy S24, and much more. Free delivery and 12-month warranty.',
        'button1_text': 'Explore products',
        'button1_link': '/produit',
        'button2_text': 'View promos',
        'button2_link': '/produit?promo=true',
        'is_active': True
    }
)
if created:
    print(f"   ✓ Section Hero créée: {hero.title}")
else:
    print(f"   - Section Hero existe déjà")

# 11. Créer les fonctionnalités (features)
print("11. Création des fonctionnalités...")
features_data = [
    {'icon': 'truck', 'title': 'Free Delivery', 'description': 'From 50,000 FCFA', 'order': 1},
    {'icon': 'shield', 'title': '12-Month Warranty', 'description': 'On all products', 'order': 2},
    {'icon': 'headphones', 'title': '24/7 Support', 'description': 'Dedicated assistance', 'order': 3},
    {'icon': 'credit-card', 'title': 'Secure Payment', 'description': 'Mobile Money & CB', 'order': 4},
]

for feat_data in features_data:
    feature, created = FeatureItem.objects.get_or_create(
        title=feat_data['title'],
        defaults={
            'icon': feat_data['icon'],
            'description': feat_data['description'],
            'order': feat_data['order'],
            'is_active': True
        }
    )
    if created:
        print(f"   ✓ Fonctionnalité créée: {feature.title}")
    else:
        print(f"   - Fonctionnalité existe déjà: {feature.title}")

# 12. Créer les cartes solutions
print("12. Création des cartes solutions...")
solutions_data = [
    {'title': 'Premium Smartphones', 'description': 'The latest iPhone & Samsung models', 'icon': 'smartphone', 'link': '/produit?category=1', 'bg_gradient': 'from-gray-800 to-gray-900', 'order': 1},
    {'title': 'Tech Accessories', 'description': 'Cases, chargers, headphones...', 'icon': 'headphones', 'link': '/produit?category=2', 'bg_gradient': 'from-gray-700 to-gray-800', 'order': 2},
    {'title': 'Computers', 'description': 'Powerful laptops and PCs', 'icon': 'monitor', 'link': '/produit?category=3', 'bg_gradient': 'from-gray-600 to-gray-700', 'order': 3},
    {'title': 'Promotions', 'description': "Up to -50% on a selection", 'icon': 'flame', 'link': '/produit?promo=true', 'bg_gradient': 'from-red-500 to-red-600', 'order': 4},
]

for sol_data in solutions_data:
    solution, created = SolutionCard.objects.get_or_create(
        title=sol_data['title'],
        defaults={
            'description': sol_data['description'],
            'icon': sol_data['icon'],
            'link': sol_data['link'],
            'bg_gradient': sol_data['bg_gradient'],
            'order': sol_data['order'],
            'is_active': True
        }
    )
    if created:
        print(f"   ✓ Carte solution créée: {solution.title}")
    else:
        print(f"   - Carte solution existe déjà: {solution.title}")

print("\n=== Données de test créées avec succès! ===")
print("\nComptes utilisateurs:")
print("  - Admin: admin / admin123")
print("  - Test:  testuser / test123")
print(f"\nProduits créés: {Product.objects.count()}")
print(f"Marques créées: {Brand.objects.count()}")
print(f"Catégories créées: {Category.objects.count()}")
print(f"Annonces créées: {Announcement.objects.filter(is_active=True).count()}")
