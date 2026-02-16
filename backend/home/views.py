from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics
from .models import Banner, Category, Announcement
from .serializers import BannerSerializer, CategorySerializer, AnnouncementSerializer

# View pour les bannières
class BannerView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

# View pour les catégories
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# View pour les annonces défilantes (lecture publique)
class AnnouncementListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AnnouncementSerializer
    
    def get_queryset(self):
        try:
            return Announcement.objects.filter(is_active=True)
        except Exception:
            return Announcement.objects.none()
    
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception:
            # Retourner une liste vide si la table n'existe pas encore
            return Response([])

# View pour gérer les annonces (admin)
class AnnouncementAdminView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
