from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('banner/', views.BannerView.as_view(), name='banner'),  # /api/home/banner/
    path('categories/', views.CategoriesView.as_view(), name='categories'),  # /api/home/categories/
    path('announcements/', views.AnnouncementListView.as_view(), name='announcements'),  # /api/home/announcements/
    path('announcements/admin/', views.AnnouncementAdminView.as_view(), name='announcements-admin'),  # /api/home/announcements/admin/
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),  # /api/home/announcements/<id>/
]
