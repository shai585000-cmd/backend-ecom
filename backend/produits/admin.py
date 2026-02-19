from django.contrib import admin
from .models import Product, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'stock', 'is_featured', 'promotion', 'created_at']
    list_filter = ['brand', 'condition', 'is_featured', 'promotion', 'created_at']
    search_fields = ['name', 'model_name', 'description']
    ordering = ['-created_at']
    list_per_page = 20
    raw_id_fields = ['user']
    
    actions = ['mark_featured', 'unmark_featured', 'activate_promotion', 'deactivate_promotion']
    
    @admin.action(description="Mettre en vedette")
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} produit(s) mis en vedette.")
    
    @admin.action(description="Retirer de la vedette")
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} produit(s) retire(s) de la vedette.")
    
    @admin.action(description="Activer la promotion")
    def activate_promotion(self, request, queryset):
        updated = queryset.update(promotion=True)
        self.message_user(request, f"Promotion activee pour {updated} produit(s).")
    
    @admin.action(description="Desactiver la promotion")
    def deactivate_promotion(self, request, queryset):
        updated = queryset.update(promotion=False)
        self.message_user(request, f"Promotion desactivee pour {updated} produit(s).")
    
    fieldsets = (
        ('Images du produit', {
            'fields': ('image', 'image_2', 'image_3', 'image_4'),
        }),
        ('Informations principales', {
            'fields': ('name', 'model_name', 'brand', 'categorie', 'description'),
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock', 'promotion', 'promotion_price', 'is_featured'),
        }),
        ('Caracteristiques', {
            'fields': ('condition', 'color', 'dual_sim'),
            'classes': ('collapse',),
        }),
        ('Specifications techniques', {
            'fields': ('ram', 'storage', 'screen_size', 'battery_capacity', 'operating_system', 'network'),
            'classes': ('collapse',),
        }),
        ('Camera', {
            'fields': ('main_camera', 'front_camera'),
            'classes': ('collapse',),
        }),
        ('Autres', {
            'fields': ('user', 'views'),
            'classes': ('collapse',),
        }),
    )
