from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('banner/', views.BannerView.as_view(), name='banner'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcements'),
    path('announcements/admin/', views.AnnouncementAdminView.as_view(), name='announcements-admin'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('hero/', views.HeroSectionView.as_view(), name='hero'),
    path('hero/admin/<int:pk>/', views.HeroSectionAdminView.as_view(), name='hero-admin'),
    path('features/', views.FeatureItemView.as_view(), name='features'),
    path('features/admin/', views.FeatureItemAdminView.as_view(), name='features-admin'),
    path('features/admin/<int:pk>/', views.FeatureItemDetailView.as_view(), name='feature-detail'),
    path('solutions/', views.SolutionCardView.as_view(), name='solutions'),
    path('solutions/admin/', views.SolutionCardAdminView.as_view(), name='solutions-admin'),
    path('solutions/admin/<int:pk>/', views.SolutionCardDetailView.as_view(), name='solution-detail'),
]
