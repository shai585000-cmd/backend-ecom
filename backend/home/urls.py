from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('banner/', views.BannerView.as_view(), name='banner'),  # /api/banner/
    path('categories/', views.CategoriesView.as_view(), name='categories'),  # /api/categories/
]
