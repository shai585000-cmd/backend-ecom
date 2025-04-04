from django.contrib import admin
from .models import Banner, Category

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'link', 'created_at')  # Affiche les champs principaux du modèle
    search_fields = ('title',)  # Permet de rechercher par titre
    list_filter = ('created_at',)  # Permet de filtrer par date de création

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')  # Affiche les champs principaux du modèle
    search_fields = ('name',)  # Permet de rechercher par nom de catégorie
    list_filter = ('created_at',)  # Permet de filtrer par date de création

# Enregistrement des modèles dans l'admin
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
