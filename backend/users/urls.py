from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


app_name = "users"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/<int:pk>/', views.DashboardProfile.as_view(), name='dashboard-profile'),
    # Nouveaux endpoints pour le profil
    path('me/', views.CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    # Google OAuth
    path('google/login/', views.GoogleLoginView.as_view(), name='google-login'),
    path('google/callback/', views.GoogleCallbackView.as_view(), name='google-callback'),
]
