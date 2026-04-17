import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ['DATABASE_URL'] = "postgresql://postgres:Offoange%4019@db.cnnilqjdfkbidufnvnyn.supabase.co:5432/postgres?sslmode=require"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from backend.home.models import SolutionCard, Category

print("=== Mise à jour des SolutionCard (liens de catégories) ===\n")

# Récupérer les catégories pour connaître leurs IDs
categories = Category.objects.all()
print("Catégories actuelles:")
for cat in categories:
    print(f"   - {cat.name}: id={cat.id}")

print("\nMise à jour des liens SolutionCard...")

# Mettre à jour Tech Accessories (Accessoires = id 2)
try:
    tech_acc = SolutionCard.objects.get(title='Tech Accessories')
    tech_acc.link = '/produit?category=2'
    tech_acc.save()
    print(f"   ✓ Tech Accessories mis à jour: {tech_acc.link}")
except SolutionCard.DoesNotExist:
    print(f"   - Tech Accessories non trouvé")

# Mettre à jour Computers (Ordinateurs = id 7)
try:
    computers = SolutionCard.objects.get(title='Computers')
    computers.link = '/produit?category=7'
    computers.save()
    print(f"   ✓ Computers mis à jour: {computers.link}")
except SolutionCard.DoesNotExist:
    print(f"   - Computers non trouvé")

print("\n=== Terminé ===")
