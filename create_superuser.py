"""
Script pour creer un superuser sur la base de donnees distante
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Parametres du superuser
USERNAME = 'admin'
EMAIL = 'admin@ivoiremarket.com'
PASSWORD = 'Admin123!'

# Verifier si le superuser existe deja
if User.objects.filter(username=USERNAME).exists():
    print(f"Le superuser '{USERNAME}' existe deja!")
    user = User.objects.get(username=USERNAME)
    # Mettre a jour le mot de passe
    user.set_password(PASSWORD)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"Mot de passe mis a jour.")
else:
    # Creer le superuser
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD
    )
    print(f"Superuser cree avec succes!")

print(f"\n=== IDENTIFIANTS ADMIN ===")
print(f"URL: https://backend-ecom-4mnz.onrender.com/admin/")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
