from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    nom_cli = models.CharField(blank=True, max_length=255)
    commerçant = models.BooleanField(default=False, blank=True)
    numero_cli = models.CharField(blank=True, max_length=255)
    adresse_cli = models.CharField(blank=True, max_length=255)
    ville_cli = models.CharField(blank=True, max_length=255)
    code_postal_cli = models.CharField(blank=True, max_length=255)
    pays_cli = models.CharField(blank=True, max_length=255)
    logo_vendeur = models.ImageField(upload_to='vendeur_logos/', blank=True, null=True)
    image_vendeur = models.ImageField(upload_to='vendeur_images/', blank=True, null=True)
    site_web_vendeur = models.URLField(blank=True, null=True)
    telephone_vendeur = models.CharField(blank=True, max_length=255)
    email_vendeur = models.EmailField(blank=True, max_length=255)
    description_vendeur = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    boutique_description = models.TextField(blank=True)
    

    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})
    



class production(AbstractUser):
    name_prod = models.CharField(blank=True, max_length=255)
    
    # Redéfinir les relations pour éviter les conflits de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='production_user_set',  # Nom inverse personnalisé
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='production_user_permissions',  # Nom inverse personnalisé
        blank=True
    )