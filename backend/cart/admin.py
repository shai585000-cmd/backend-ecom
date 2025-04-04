from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Le nombre d'éléments par défaut dans l'interface d'administration

class CartAdmin(admin.ModelAdmin):

    list_display = ('user', 'created_at')  # Affichez l'utilisateur et la date de création
    search_fields = ('user__username',)  # Permet de rechercher un panier par le nom d'utilisateur
    inlines = [CartItemInline]  # Affiche les éléments du panier directement dans l'interface d'administration du panier

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','price')  # Affichez le panier, le produit, la quantité et le prix
    search_fields = ('product',)  # Permet de rechercher un élément par son nom
    list_filter = ('cart',)  # Filtrer par panier dans l'interface d'administration
    fields = ('cart', 'product', 'price')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
