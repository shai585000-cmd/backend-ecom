from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django.views import View
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from backend.users.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, UpdateView, RedirectView
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, serializers
from .serializers import (
    LoginSerializer, UserSerializer, DashboardSerializer,
    UserProfileSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer
)
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        print("Données reçues:", request.data)  # Debug
        serializer = self.serializer_class(data=request.data)
        
        try:
            if not serializer.is_valid():
                print("Erreurs de validation:", serializer.errors)  # Debug
                return Response({
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data['user']
            print(f"Utilisateur authentifié: {user}")  # Debug
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Connexion réussie',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'nom_cli': user.nom_cli,  
                    'commerçant': user.commerçant,


                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
            
        except Exception as e:
            print(f"Erreur inattendue: {str(e)}")  # Debug
            return Response({
                'error': f'Une erreur est survenue lors de la connexion: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()  # Sauvegarde l'utilisateur créé
            refresh = RefreshToken.for_user(user)

            return Response({
                'message': 'Inscription réussie',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nom_cli': user.nom_cli,
                    'commerçant': user.commerçant,
                    'numero_cli': user.numero_cli,
                    'adresse_cli': user.adresse_cli,
                    'ville_cli': user.ville_cli,
                    'code_postal_cli': user.code_postal_cli,
                    'pays_cli': user.pays_cli,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=HTTP_201_CREATED)

        return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)



# View pour afficher le profil de l'utilisateur
class UserProfileView(View):
    @login_required
    def get(self, request, *args, **kwargs):
        return JsonResponse({
            'username': request.user.username,
            'email': request.user.email,
            'nom_cli': request.user.nom_cli
        })
    

    
class DashboardProfile(generics.RetrieveAPIView):
    serializer_class = DashboardSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return User.objects.get(id=self.kwargs['pk'])


class CurrentUserProfileView(APIView):
    """Recuperer et mettre a jour le profil de l'utilisateur connecte"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profil mis a jour avec succes',
                'user': UserProfileSerializer(request.user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)


class ChangePasswordView(APIView):
    """Changer le mot de passe de l'utilisateur connecte"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'message': 'Mot de passe modifie avec succes'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import redirect
from django.conf import settings

class GoogleLoginView(View):
    """Rediriger vers la page de connexion Google"""
    def get(self, request):
        return redirect('/accounts/google/login/')


class GoogleCallbackView(APIView):
    """Callback apres authentification Google - genere les tokens JWT"""
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            refresh = RefreshToken.for_user(user)
            frontend_url = getattr(settings, 'GOOGLE_OAUTH_CALLBACK_URL', 'https://frontend-ecom-weld.vercel.app/')
            
            # Rediriger vers le frontend avec les tokens
            redirect_url = f"{frontend_url}?access={str(refresh.access_token)}&refresh={str(refresh)}"
            return redirect(redirect_url)
        
        return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)


from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

class GoogleAuthView(APIView):
    """Authentification Google cote client - recoit le credential et cree/connecte l'utilisateur"""
    permission_classes = [AllowAny]

    def post(self, request):
        credential = request.data.get('credential')
        
        if not credential:
            return Response({'error': 'Credential manquant'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Verifier le token Google
            idinfo = id_token.verify_oauth2_token(
                credential,
                google_requests.Request(),
                '427788449898-u3i5tqe9dnpvice4kjr3rp06vbfou4sv.apps.googleusercontent.com'
            )
            
            email = idinfo.get('email')
            name = idinfo.get('name', '')
            
            # Chercher ou creer l'utilisateur
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'nom_cli': name,
                }
            )
            
            # Generer les tokens JWT
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Connexion reussie',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'nom_cli': user.nom_cli,
                },
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            })
            
        except ValueError as e:
            return Response({'error': f'Token invalide: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
