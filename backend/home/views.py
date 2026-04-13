from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

# Create your views here.
from rest_framework import generics
from .models import Banner, Category, Announcement, HeroSection, FeatureItem, SolutionCard
from .serializers import (BannerSerializer, CategorySerializer, AnnouncementSerializer,
                          HeroSectionSerializer, FeatureItemSerializer, SolutionCardSerializer)

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


# View pour la section Hero (lecture publique, écriture admin)
class HeroSectionView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HeroSectionSerializer

    def get_queryset(self):
        return HeroSection.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset.first())
            return Response(serializer.data)
        return Response({})


class HeroSectionAdminView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = HeroSection.objects.all()
    serializer_class = HeroSectionSerializer


# View pour les fonctionnalités (Livraison, Garantie, etc.)
class FeatureItemView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = FeatureItemSerializer

    def get_queryset(self):
        return FeatureItem.objects.filter(is_active=True)


class FeatureItemAdminView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = FeatureItem.objects.all()
    serializer_class = FeatureItemSerializer


class FeatureItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = FeatureItem.objects.all()
    serializer_class = FeatureItemSerializer


# View pour les cartes solutions
class SolutionCardView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SolutionCardSerializer

    def get_queryset(self):
        return SolutionCard.objects.filter(is_active=True)


class SolutionCardAdminView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = SolutionCard.objects.all()
    serializer_class = SolutionCardSerializer


class SolutionCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = SolutionCard.objects.all()
    serializer_class = SolutionCardSerializer
