# products/urls.py
from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),  # /api/products/
    path('products/<int:id>/', views.ProductDetailView.as_view(), name='product-detail'),  # /api/products/<id>/
    path('featured-products/', views.FeaturedProductsView.as_view(), name='featured-products'),  # /api/featured-products/
    path('products/create/', views.ProductCreateView.as_view(), name='product-create'),  # /api/products/create/
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),  # /api/products/<id>/update/
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),  # /api/products/<id>/delete/
    path('products/promotion/', views.PromotionProductsView.as_view(), name='promotion-products'),  # /api/products/promotion/
    path('products/nosproduits/', views.NosProduitsView.as_view(), name='nos-produits'),  # /api/products/nos-produits/
    path('products/dashboard/<str:nom_cli>/', views.DashboardProduits.as_view(), name='dashboard-produits'),  # /api/products/dashboard/
]
