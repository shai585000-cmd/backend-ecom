from django.contrib import admin
from django.contrib import messages
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    fields = ['product_name', 'quantity', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'get_client', 'status', 'total_amount', 'shipping_city', 'created_at']
    list_filter = ['status', 'created_at', 'shipping_city']
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_phone', 'shipping_city']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'order_number']
    list_per_page = 25
    ordering = ['-created_at']
    
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    def get_client(self, obj):
        if obj.user:
            return obj.user.username
        return obj.guest_name or 'Invite'
    get_client.short_description = 'Client'
    get_client.admin_order_field = 'user__username'
    
    @admin.action(description="Confirmer les commandes selectionnees")
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f"{updated} commande(s) confirmee(s).", messages.SUCCESS)
    
    @admin.action(description="Passer en traitement")
    def mark_as_processing(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='processing')
        self.message_user(request, f"{updated} commande(s) en traitement.", messages.SUCCESS)
    
    @admin.action(description="Marquer comme expediees")
    def mark_as_shipped(self, request, queryset):
        updated = queryset.filter(status='processing').update(status='shipped')
        self.message_user(request, f"{updated} commande(s) expediee(s).", messages.SUCCESS)
    
    @admin.action(description="Marquer comme livrees")
    def mark_as_delivered(self, request, queryset):
        updated = queryset.filter(status='shipped').update(status='delivered')
        self.message_user(request, f"{updated} commande(s) livree(s).", messages.SUCCESS)
    
    @admin.action(description="Annuler les commandes selectionnees")
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.exclude(status__in=['delivered', 'cancelled', 'refunded']).update(status='cancelled')
        self.message_user(request, f"{updated} commande(s) annulee(s).", messages.WARNING)
    
    fieldsets = (
        ('Informations commande', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Livraison', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_phone')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__status']
    search_fields = ['product_name', 'order__order_number']
