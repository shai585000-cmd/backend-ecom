import os
import sys
import django

# Configuration
LOCAL_DB = "postgres://postgres:offoange@localhost:5432/base"
REMOTE_DB = "postgresql://ecommerce_gf50_user:eyefaetl2KIbxAZJ2EemVaCzLLzVD8Yg@dpg-d4kvo8v5r7bs73clpe9g-a.oregon-postgres.render.com/ecommerce_gf50"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# Export depuis la base locale
print("=== EXPORT depuis la base locale ===")
os.environ['DATABASE_URL'] = LOCAL_DB
django.setup()

from django.core import serializers
from django.apps import apps

# Liste des modèles à exporter (dans l'ordre des dépendances)
models_to_export = []
for app_config in apps.get_app_configs():
    if app_config.name in ['django.contrib.contenttypes', 'django.contrib.sessions', 
                           'django.contrib.admin', 'debug_toolbar']:
        continue
    for model in app_config.get_models():
        models_to_export.append(model)

# Exporter les données
all_data = []
for model in models_to_export:
    try:
        queryset = model.objects.all()
        if queryset.exists():
            data = serializers.serialize('python', queryset, use_natural_foreign_keys=True, use_natural_primary_keys=True)
            all_data.extend(data)
            print(f"  Exporté: {model._meta.label} ({queryset.count()} objets)")
    except Exception as e:
        print(f"  Erreur {model._meta.label}: {e}")

print(f"\nTotal: {len(all_data)} objets exportés")

# Sauvegarder en JSON propre
import json
with open('data_clean.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

print("\n=== Fichier data_clean.json créé ===")
print("Exécutez maintenant: python manage.py loaddata data_clean.json")
print(f"Avec DATABASE_URL={REMOTE_DB}")
