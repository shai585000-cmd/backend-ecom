from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','id','user','views','image','categorie','promotion','promotion_price','name', 'price', 'is_featured', 'created_at', 'updated_at')  # Affiche les champs principaux du modèle
    search_fields = ('name', 'description')  # Permet de rechercher par nom et description
    list_filter = ('is_featured', 'created_at')  # Permet de filtrer par produit en vedette et date de création
    ordering = ('-created_at',)  # Trie les produits par date de création, du plus récent au plus ancien

# Enregistrement du modèle Product dans l'admin
admin.site.register(Product, ProductAdmin)
