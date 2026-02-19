from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum
from .models import Product, Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['logo_preview', 'name', 'products_count', 'is_active']
    search_fields = ['name']
    list_filter = ['is_active']
    list_editable = ['is_active']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: contain; border-radius: 4px; background: #f3f4f6; padding: 4px;"/>',
                obj.logo.url
            )
        return format_html('<span style="color: #9ca3af;">Pas de logo</span>')
    logo_preview.short_description = "Logo"
    
    def products_count(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background: #e0e7ff; color: #3730a3; padding: 3px 10px; border-radius: 12px; font-size: 12px;">{} produit{}</span>',
            count, 's' if count > 1 else ''
        )
    products_count.short_description = "Produits"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 
        'product_info', 
        'price_display', 
        'stock_badge', 
        'status_badges',
        'views_count',
        'quick_actions'
    ]
    list_filter = ['brand', 'condition', 'is_featured', 'promotion', 'stock', 'created_at']
    search_fields = ['name', 'model_name', 'description']
    ordering = ['-created_at']
    readonly_fields = ['views', 'created_at', 'updated_at', 'image_preview_large', 'product_stats']
    list_per_page = 20
    list_select_related = ['brand', 'categorie']
    date_hierarchy = 'created_at'
    
    # Actions rapides
    actions = ['mark_featured', 'unmark_featured', 'activate_promotion', 'deactivate_promotion', 'duplicate_products']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);"/>',
                obj.image.url if hasattr(obj.image, 'url') else obj.image
            )
        return format_html(
            '<div style="width: 60px; height: 60px; background: #f3f4f6; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #9ca3af; font-size: 20px;">📷</div>'
        )
    image_preview.short_description = "Photo"
    
    def product_info(self, obj):
        brand_name = obj.brand.name if obj.brand else "Sans marque"
        return format_html(
            '<div style="line-height: 1.4;">'
            '<strong style="color: #111827; font-size: 14px;">{}</strong><br/>'
            '<span style="color: #6b7280; font-size: 12px;">{}</span>'
            '</div>',
            obj.name[:40] + '...' if len(obj.name) > 40 else obj.name,
            brand_name
        )
    product_info.short_description = "Produit"
    product_info.admin_order_field = 'name'
    
    def price_display(self, obj):
        if obj.promotion and obj.promotion_price:
            return format_html(
                '<div style="line-height: 1.4;">'
                '<span style="text-decoration: line-through; color: #9ca3af; font-size: 11px;">{:,.0f}</span><br/>'
                '<strong style="color: #dc2626; font-size: 14px;">{:,.0f} FCFA</strong>'
                '</div>',
                obj.price, obj.promotion_price
            )
        return format_html(
            '<strong style="color: #111827; font-size: 14px;">{:,.0f} FCFA</strong>',
            obj.price
        )
    price_display.short_description = "Prix"
    price_display.admin_order_field = 'price'
    
    def stock_badge(self, obj):
        if obj.stock == 0:
            return format_html(
                '<span style="background: #fee2e2; color: #dc2626; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;">Rupture</span>'
            )
        elif obj.stock <= 5:
            return format_html(
                '<span style="background: #fef3c7; color: #d97706; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;">{} restant{}</span>',
                obj.stock, 's' if obj.stock > 1 else ''
            )
        return format_html(
            '<span style="background: #d1fae5; color: #059669; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 500;">{} en stock</span>',
            obj.stock
        )
    stock_badge.short_description = "Stock"
    stock_badge.admin_order_field = 'stock'
    
    def status_badges(self, obj):
        badges = []
        if obj.is_featured:
            badges.append('<span style="background: #fef3c7; color: #d97706; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-right: 4px;">⭐ Vedette</span>')
        if obj.promotion:
            badges.append('<span style="background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 4px; font-size: 11px;">🏷️ Promo</span>')
        return format_html(''.join(badges)) if badges else format_html('<span style="color: #d1d5db;">-</span>')
    status_badges.short_description = "Statut"
    
    def views_count(self, obj):
        return format_html(
            '<span style="color: #6b7280; font-size: 12px;">👁️ {}</span>',
            obj.views
        )
    views_count.short_description = "Vues"
    views_count.admin_order_field = 'views'
    
    def quick_actions(self, obj):
        return format_html(
            '<a href="/admin/produits/product/{}/change/" '
            'style="background: #111827; color: white; padding: 6px 12px; border-radius: 6px; '
            'text-decoration: none; font-size: 12px; font-weight: 500;">Modifier</a>',
            obj.pk
        )
    quick_actions.short_description = "Action"
    
    def image_preview_large(self, obj):
        images = [obj.image, obj.image_2, obj.image_3, obj.image_4]
        html = '<div style="display: flex; gap: 10px; flex-wrap: wrap;">'
        for i, img in enumerate(images, 1):
            if img:
                html += f'<div style="text-align: center;"><img src="{img.url if hasattr(img, "url") else img}" style="width: 150px; height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/><br/><span style="font-size: 11px; color: #6b7280;">Image {i}</span></div>'
        html += '</div>'
        return format_html(html) if any(images) else format_html('<span style="color: #9ca3af;">Aucune image</span>')
    image_preview_large.short_description = "Aperçu des images"
    
    def product_stats(self, obj):
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; display: flex; gap: 30px;">'
            '<div><span style="color: #6b7280; font-size: 12px;">Vues</span><br/><strong style="font-size: 20px; color: #111827;">{}</strong></div>'
            '<div><span style="color: #6b7280; font-size: 12px;">Stock</span><br/><strong style="font-size: 20px; color: #111827;">{}</strong></div>'
            '<div><span style="color: #6b7280; font-size: 12px;">Créé le</span><br/><strong style="font-size: 14px; color: #111827;">{}</strong></div>'
            '</div>',
            obj.views, obj.stock, obj.created_at.strftime('%d/%m/%Y') if obj.created_at else '-'
        )
    product_stats.short_description = "Statistiques"
    
    # Actions en masse
    @admin.action(description="Mettre en vedette")
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"{updated} produit(s) mis en vedette.")
    
    @admin.action(description="Retirer de la vedette")
    def unmark_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f"{updated} produit(s) retiré(s) de la vedette.")
    
    @admin.action(description="Activer la promotion")
    def activate_promotion(self, request, queryset):
        updated = queryset.update(promotion=True)
        self.message_user(request, f"Promotion activée pour {updated} produit(s). N'oubliez pas de définir le prix promo!")
    
    @admin.action(description="Désactiver la promotion")
    def deactivate_promotion(self, request, queryset):
        updated = queryset.update(promotion=False)
        self.message_user(request, f"Promotion désactivée pour {updated} produit(s).")
    
    @admin.action(description="Dupliquer les produits")
    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.name = f"Copie de {product.name}"
            product.save()
        self.message_user(request, f"{queryset.count()} produit(s) dupliqué(s).")
    
    fieldsets = (
        ('Images du produit', {
            'fields': ('image_preview_large', 'image', 'image_2', 'image_3', 'image_4'),
            'description': 'Ajoutez jusqu\'à 4 photos de votre produit. La première image sera l\'image principale.'
        }),
        ('Informations principales', {
            'fields': ('name', 'model_name', 'brand', 'categorie', 'description'),
            'description': 'Remplissez les informations de base du produit.'
        }),
        ('Prix et Stock', {
            'fields': ('price', 'stock', 'promotion', 'promotion_price', 'is_featured'),
            'description': 'Définissez le prix et la quantité disponible.'
        }),
        ('Caractéristiques', {
            'fields': ('condition', 'color', 'dual_sim'),
            'classes': ('collapse',),
            'description': 'État et couleur du produit.'
        }),
        ('Spécifications techniques', {
            'fields': ('ram', 'storage', 'screen_size', 'battery_capacity', 'operating_system', 'network'),
            'classes': ('collapse',),
            'description': 'Détails techniques (optionnel).'
        }),
        ('Caméra', {
            'fields': ('main_camera', 'front_camera'),
            'classes': ('collapse',),
        }),
        ('Statistiques', {
            'fields': ('product_stats', 'user'),
            'classes': ('collapse',),
        }),
    )
