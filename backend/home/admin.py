from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, Category

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'link', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    readonly_fields = ('image_preview_large',)
    
    fieldsets = (
        ('Informations de la banniere', {
            'fields': ('title', 'link')
        }),
        ('Image', {
            'fields': ('image', 'image_preview_large')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Apercu"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 300px; border-radius: 8px;"/>',
                obj.image.url
            )
        return "-"
    image_preview_large.short_description = "Apercu de l'image"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')  # Affiche les champs principaux du modèle
    search_fields = ('name',)  # Permet de rechercher par nom de catégorie
    list_filter = ('created_at',)  # Permet de filtrer par date de création

# Enregistrement des modèles dans l'admin
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
