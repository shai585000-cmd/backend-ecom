from rest_framework import serializers
from .models import Banner, Category, Announcement, HeroSection, FeatureItem, SolutionCard

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Banner
        fields = ['id', 'title', 'image', 'link', 'created_at']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name', 'description', 'created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'text', 'emoji', 'is_active', 'order', 'created_at']


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ['id', 'badge_text', 'title', 'title_highlight', 'description',
                  'button1_text', 'button1_link', 'button2_text', 'button2_link', 'updated_at']


class FeatureItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureItem
        fields = ['id', 'icon', 'title', 'description', 'order']


class SolutionCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionCard
        fields = ['id', 'title', 'description', 'icon', 'link', 'bg_gradient', 'order']
