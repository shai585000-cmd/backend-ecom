import os
import sys
import django

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ['DATABASE_URL'] = "postgresql://postgres:Offoange%4019@db.cnnilqjdfkbidufnvnyn.supabase.co:5432/postgres?sslmode=require"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.contrib.auth import get_user_model
from backend.produits.models import Product, Brand
from backend.home.models import Category

User = get_user_model()

print("=== Création des produits Computers ===\n")

# Récupérer l'admin
admin_user = User.objects.get(nom_cli='admin')

# Créer la catégorie si elle n'existe pas
computers_cat, created = Category.objects.get_or_create(
    name='Ordinateurs',
    defaults={'description': 'Laptops et PCs puissants'}
)
if created:
    print(f"   ✓ Catégorie créée: {computers_cat.name}")
else:
    print(f"   - Catégorie existante: {computers_cat.name}")

# Créer les marques
brands_to_create = ['Apple', 'HP', 'Dell', 'Lenovo', 'Asus', 'MSI', 'Acer']
for brand_name in brands_to_create:
    Brand.objects.get_or_create(name=brand_name)

print("\nCréation des produits ordinateurs...")

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
    },
]

created_count = 0
for prod_data in computers_data:
    product_name = prod_data['name']
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
        
        if created:
            created_count += 1
            print(f"   ✓ {product.name} - {product.price}€")
        else:
            print(f"   - Existe déjà: {product.name}")
    except Exception as e:
        print(f"   ✗ Erreur pour {product_name}: {e}")

print(f"\n=== {created_count} ordinateurs créés avec succès! ===")
print(f"Total produits en base: {Product.objects.count()}")
