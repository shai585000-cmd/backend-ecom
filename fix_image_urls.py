"""
Script pour corriger les URLs d'images dans la base de donnees.
Corrige les URLs avec triple slash https:///
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from backend.produits.models import Product

print("=" * 50)
print("CORRECTION DES URLs D'IMAGES")
print("=" * 50)

products = Product.objects.all()
fixed_count = 0

for product in products:
    if product.image:
        image_str = str(product.image)
        
        # Corriger les triple slashes
        if 'https:///' in image_str:
            url = image_str.replace('https:///', 'https://')
            print(f"Ancien: {image_str}")
            print(f"Nouveau: {url}")
            print("-" * 30)
            product.image = url
            product.save()
            fixed_count += 1

print(f"\n{fixed_count} image(s) corrigee(s)")
