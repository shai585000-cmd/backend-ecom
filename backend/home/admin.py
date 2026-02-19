from django.contrib import admin
from django.utils.html import format_html
from .models import Banner, Category, Announcement


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'link_display', 'created_at_formatted')
    search_fields = ('title',)
    list_filter = ('created_at',)
    readonly_fields = ('image_preview_large',)
    list_per_page = 10
    
    fieldsets = (
        ('🖼️ Image de la bannière', {
            'fields': ('image', 'image_preview_large'),
            'description': 'Téléchargez une image pour la bannière du site. Taille recommandée: 1920x600 pixels.'
        }),
        ('📝 Informations', {
            'fields': ('title', 'link'),
            'description': 'Le titre est optionnel. Le lien permet de rediriger vers une page quand on clique sur la bannière.'
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 120px; height: 60px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">Pas d\'image</span>')
    image_preview.short_description = "Aperçu"
    
    def link_display(self, obj):
        if obj.link:
            return format_html(
                '<a href="{}" target="_blank" style="color: #4f46e5; text-decoration: none;">🔗 Voir le lien</a>',
                obj.link
            )
        return format_html('<span style="color: #9ca3af;">Aucun lien</span>')
    link_display.short_description = "Lien"
    
    def created_at_formatted(self, obj):
        return format_html(
            '<span style="color: #6b7280; font-size: 13px;">{}</span>',
            obj.created_at.strftime('%d/%m/%Y')
        )
    created_at_formatted.short_description = "Date"
    
    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100%; max-height: 300px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return format_html('<span style="color: #9ca3af;">Aucune image téléchargée</span>')
    image_preview_large.short_description = "Aperçu de l'image"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_short', 'products_count', 'created_at_formatted')
    search_fields = ('name',)
    list_filter = ('created_at',)
    list_per_page = 20
    
    fieldsets = (
        ('📂 Informations de la catégorie', {
            'fields': ('name', 'description'),
            'description': 'Créez des catégories pour organiser vos produits (ex: Smartphones, Accessoires, etc.)'
        }),
    )
    
    def description_short(self, obj):
        if obj.description:
            text = obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
            return format_html('<span style="color: #6b7280;">{}</span>', text)
        return format_html('<span style="color: #d1d5db;">Pas de description</span>')
    description_short.short_description = "Description"
    
    def products_count(self, obj):
        count = obj.product_set.count() if hasattr(obj, 'product_set') else 0
        return format_html(
            '<span style="background: #e0e7ff; color: #3730a3; padding: 3px 10px; border-radius: 12px; font-size: 12px;">{} produit{}</span>',
            count, 's' if count > 1 else ''
        )
    products_count.short_description = "Produits"
    
    def created_at_formatted(self, obj):
        return format_html(
            '<span style="color: #6b7280; font-size: 13px;">{}</span>',
            obj.created_at.strftime('%d/%m/%Y')
        )
    created_at_formatted.short_description = "Date"


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('announcement_preview', 'is_active_badge', 'order', 'created_at_formatted')
    list_editable = ('order',)
    search_fields = ('text',)
    list_filter = ('is_active', 'created_at')
    ordering = ('order', '-created_at')
    list_per_page = 20
    
    fieldsets = (
        ('📢 Annonce', {
            'fields': ('emoji', 'text', 'is_active', 'order'),
            'description': 'Créez des annonces qui s\'affichent en haut du site (ex: promotions, nouveautés, etc.)'
        }),
    )
    
    def announcement_preview(self, obj):
        return format_html(
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-size: 20px;">{}</span>'
            '<span style="color: #374151;">{}</span>'
            '</div>',
            obj.emoji or '📢',
            obj.text[:60] + '...' if len(obj.text) > 60 else obj.text
        )
    announcement_preview.short_description = "Annonce"
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background: #d1fae5; color: #059669; padding: 4px 10px; border-radius: 12px; font-size: 12px;">✓ Active</span>'
            )
        return format_html(
            '<span style="background: #f3f4f6; color: #6b7280; padding: 4px 10px; border-radius: 12px; font-size: 12px;">Inactive</span>'
        )
    is_active_badge.short_description = "Statut"
    is_active_badge.admin_order_field = 'is_active'
    
    def created_at_formatted(self, obj):
        return format_html(
            '<span style="color: #6b7280; font-size: 13px;">{}</span>',
            obj.created_at.strftime('%d/%m/%Y')
        )
    created_at_formatted.short_description = "Date"
