from django.contrib import admin
from .models import Banner, Category, Announcement, HeroSection, FeatureItem, SolutionCard


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


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'is_active', 'updated_at')
    list_editable = ('is_active',)
    fieldsets = (
        ('Contenu principal', {
            'fields': ('badge_text', 'title', 'title_highlight', 'description', 'is_active')
        }),
        ('Boutons', {
            'fields': ('button1_text', 'button1_link', 'button2_text', 'button2_link')
        }),
    )


@admin.register(FeatureItem)
class FeatureItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'description', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)


@admin.register(SolutionCard)
class SolutionCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'icon', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
