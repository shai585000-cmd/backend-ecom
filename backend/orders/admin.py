from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price', 'product_image_preview']
    fields = ['product_image_preview', 'product_name', 'quantity', 'unit_price', 'total_price']
    
    def product_image_preview(self, obj):
        if obj.product and obj.product.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;"/>',
                obj.product.image.url if hasattr(obj.product.image, 'url') else obj.product.image
            )
        return "-"
    product_image_preview.short_description = "Image"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 
        'user_info', 
        'status_badge', 
        'items_count',
        'total_amount_formatted', 
        'shipping_city', 
        'created_at_formatted',
        'quick_actions_buttons'
    ]
    list_filter = ['status', 'created_at', 'shipping_city']
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_phone', 'shipping_city']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'order_number', 'order_summary']
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_select_related = ['user']
    
    # Actions personnalisees
    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    change_list_template = 'admin/orders/order/change_list.html'
    
    def changelist_view(self, request, extra_context=None):
        """Ajoute les KPIs au contexte"""
        extra_context = extra_context or {}
        
        # Statistiques par statut
        status_counts = Order.objects.values('status').annotate(count=Count('id'))
        status_dict = {item['status']: item['count'] for item in status_counts}
        
        # Total et revenus
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Statistiques du jour
        today = timezone.now().date()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_orders = Order.objects.filter(created_at__gte=today_start).count()
        today_revenue = Order.objects.filter(
            created_at__gte=today_start,
            status__in=['confirmed', 'processing', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        today_delivered = Order.objects.filter(
            updated_at__gte=today_start,
            status='delivered'
        ).count()
        
        # Statut actuel filtre
        current_status = request.GET.get('status__exact', '')
        
        extra_context.update({
            'total_orders': total_orders,
            'pending_count': status_dict.get('pending', 0),
            'confirmed_count': status_dict.get('confirmed', 0),
            'processing_count': status_dict.get('processing', 0),
            'shipped_count': status_dict.get('shipped', 0),
            'delivered_count': status_dict.get('delivered', 0),
            'cancelled_count': status_dict.get('cancelled', 0),
            'refunded_count': status_dict.get('refunded', 0),
            'total_revenue': "{:,.0f}".format(total_revenue),
            'today_orders': today_orders,
            'today_revenue': "{:,.0f}".format(today_revenue),
            'today_delivered': today_delivered,
            'current_status': current_status,
        })
        
        return super().changelist_view(request, extra_context=extra_context)
    
    def user_info(self, obj):
        """Affiche les infos utilisateur"""
        if obj.user:
            email = obj.user.email or ''
            return format_html(
                '<div style="line-height: 1.4;">'
                '<strong>{}</strong><br/>'
                '<span style="color: #6b7280; font-size: 11px;">{}</span>'
                '</div>',
                obj.user.username,
                email[:25] + '...' if len(email) > 25 else email
            )
        return format_html(
            '<div style="line-height: 1.4;">'
            '<strong>{}</strong><br/>'
            '<span style="color: #6b7280; font-size: 11px;">Invite</span>'
            '</div>',
            obj.guest_name or 'Invite'
        )
    user_info.short_description = 'Client'
    user_info.admin_order_field = 'user__username'
    
    def items_count(self, obj):
        """Nombre d'articles"""
        count = obj.items.count()
        return format_html(
            '<span style="color: #6b7280; font-size: 13px;">{} article{}</span>',
            count,
            's' if count > 1 else ''
        )
    items_count.short_description = 'Articles'
    
    def status_badge(self, obj):
        """Affiche le statut de maniere professionnelle"""
        status_config = {
            'pending': {'color': '#6b7280', 'bg': '#f3f4f6'},
            'confirmed': {'color': '#1f2937', 'bg': '#e5e7eb'},
            'processing': {'color': '#1f2937', 'bg': '#e5e7eb'},
            'shipped': {'color': '#1f2937', 'bg': '#e5e7eb'},
            'delivered': {'color': '#047857', 'bg': '#d1fae5'},
            'cancelled': {'color': '#dc2626', 'bg': '#fee2e2'},
            'refunded': {'color': '#6b7280', 'bg': '#f3f4f6'},
        }
        config = status_config.get(obj.status, {'color': '#6b7280', 'bg': '#f3f4f6'})
        return format_html(
            '<span style="background: {}; color: {}; padding: 5px 10px; border-radius: 4px; font-size: 12px; font-weight: 500;">'  
            '{}</span>',
            config['bg'],
            config['color'],
            obj.get_status_display()
        )
    status_badge.short_description = 'Statut'
    status_badge.admin_order_field = 'status'
    
    def total_amount_formatted(self, obj):
        """Affiche le montant formate"""
        amount = "{:,.0f}".format(obj.total_amount)
        return format_html(
            '<span style="font-weight: 600; color: #111827;">{} FCFA</span>',
            amount
        )
    total_amount_formatted.short_description = 'Montant'
    total_amount_formatted.admin_order_field = 'total_amount'
    
    def created_at_formatted(self, obj):
        """Date formatee"""
        return format_html(
            '<div style="line-height: 1.4;">'
            '<span style="font-weight: 500;">{}</span><br/>'
            '<span style="color: #6b7280; font-size: 11px;">{}</span>'
            '</div>',
            obj.created_at.strftime('%d/%m/%Y'),
            obj.created_at.strftime('%H:%M')
        )
    created_at_formatted.short_description = 'Date'
    created_at_formatted.admin_order_field = 'created_at'
    
    def quick_actions_buttons(self, obj):
        """Boutons d'action rapide"""
        next_status = {
            'pending': ('confirmed', 'Confirmer'),
            'confirmed': ('processing', 'Traiter'),
            'processing': ('shipped', 'Expedier'),
            'shipped': ('delivered', 'Livrer'),
        }
        
        if obj.status in next_status:
            status, label = next_status[obj.status]
            return format_html(
                '<a href="/admin/orders/order/{}/change/" '
                'style="background: #111827; color: white; padding: 5px 12px; border-radius: 4px; '
                'text-decoration: none; font-size: 12px; font-weight: 500;">'  
                '{}</a>',
                obj.pk,
                label
            )
        return '-'
    quick_actions_buttons.short_description = 'Action'
    
    def order_summary(self, obj):
        """Resume de la commande pour la page de detail"""
        items_html = ""
        for item in obj.items.all():
            items_html += f"<li>{item.quantity}x {item.product_name} - {item.total_price:,.0f} FCFA</li>"
        
        return format_html(
            '<div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin: 10px 0;">'
            '<h4 style="margin: 0 0 10px 0; color: #1f2937;">Articles commandes</h4>'
            '<ul style="margin: 0; padding-left: 20px;">{}</ul>'
            '<hr style="margin: 15px 0; border: none; border-top: 1px solid #e2e8f0;"/>'
            '<strong style="font-size: 16px; color: #059669;">Total: {:,.0f} FCFA</strong>'
            '</div>',
            items_html,
            obj.total_amount
        )
    order_summary.short_description = 'Resume'
    
    # Actions rapides
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
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Resume de la commande', {
            'fields': ('order_summary',),
            'classes': ('wide',)
        }),
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
