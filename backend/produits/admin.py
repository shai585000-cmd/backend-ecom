from django.contrib import admin
from .models import Product, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price', 'condition', 'stock', 'is_featured', 'promotion', 'created_at']
    list_filter = ['brand', 'condition', 'operating_system', 'network', 'is_featured', 'promotion', 'created_at']
    search_fields = ['name', 'model_name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'model_name', 'brand', 'categorie', 'user', 'description')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3', 'image_4'),
            'classes': ('collapse',)
        }),
        ('Prix & Stock', {
            'fields': ('price', 'promotion', 'promotion_price', 'stock', 'is_featured')
        }),
        ('Caractéristiques téléphone', {
            'fields': ('condition', 'color', 'dual_sim'),
        }),
        ('Spécifications techniques', {
            'fields': ('ram', 'storage', 'screen_size', 'battery_capacity', 'operating_system', 'network'),
            'classes': ('collapse',)
        }),
        ('Caméra', {
            'fields': ('main_camera', 'front_camera'),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
