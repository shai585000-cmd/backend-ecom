from django.contrib import admin
from .models import Banner, Category, Announcement


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    list_per_page = 10


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    list_per_page = 20


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('text', 'emoji', 'is_active', 'order', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('text',)
    list_filter = ('is_active', 'created_at')
    ordering = ('order', '-created_at')
    list_per_page = 20
