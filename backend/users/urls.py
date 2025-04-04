from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


app_name = "users"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),  # /api/login/
    path('signup/', views.SignupView.as_view(), name='signup'),  # /api/signup/
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),  # /api/profile/
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # /api/token/refresh/
    path('dashboard/<int:pk>/', views.DashboardProfile.as_view(), name='dashboard-profile'),  # /api/dashboard/profile/
]
