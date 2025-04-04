from django.shortcuts import render
from rest_framework.permissions import AllowAny

# Create your views here.
from rest_framework import generics
from .models import Banner, Category
from .serializers import BannerSerializer, CategorySerializer

# View pour les bannières
class BannerView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

# View pour les catégories
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
