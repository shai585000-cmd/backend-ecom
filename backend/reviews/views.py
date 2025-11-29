from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer, ProductReviewStatsSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'product_reviews', 'product_stats']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_queryset(self):
        queryset = Review.objects.select_related('user', 'product')
        
        # Filtrer par produit
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Filtrer par note
        rating = self.request.query_params.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return Response(
            ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {"error": "Vous ne pouvez modifier que vos propres avis"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if review.user != request.user:
            return Response(
                {"error": "Vous ne pouvez supprimer que vos propres avis"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='product/(?P<product_id>[^/.]+)')
    def product_reviews(self, request, product_id=None):
        """Recuperer tous les avis d'un produit"""
        reviews = Review.objects.filter(product_id=product_id).select_related('user')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='product/(?P<product_id>[^/.]+)/stats')
    def product_stats(self, request, product_id=None):
        """Recuperer les statistiques des avis d'un produit"""
        reviews = Review.objects.filter(product_id=product_id)
        
        stats = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        
        # Distribution des notes
        distribution = {}
        for i in range(1, 6):
            count = reviews.filter(rating=i).count()
            distribution[str(i)] = count
        
        return Response({
            'average_rating': round(stats['average_rating'] or 0, 1),
            'total_reviews': stats['total_reviews'],
            'rating_distribution': distribution
        })
    
    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Recuperer les avis de l'utilisateur connecte"""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentification requise"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        reviews = Review.objects.filter(user=request.user).select_related('product')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='can-review/(?P<product_id>[^/.]+)')
    def can_review(self, request, product_id=None):
        """Verifier si l'utilisateur peut laisser un avis"""
        if not request.user.is_authenticated:
            return Response({'can_review': False, 'reason': 'non_authenticated'})
        
        # Verifier si deja un avis
        has_review = Review.objects.filter(
            user=request.user, 
            product_id=product_id
        ).exists()
        
        if has_review:
            return Response({'can_review': False, 'reason': 'already_reviewed'})
        
        return Response({'can_review': True})
