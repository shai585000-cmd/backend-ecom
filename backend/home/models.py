from django.db import models

# Create your models here.


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    """Modèle pour les annonces défilantes en haut de page"""
    text = models.CharField(max_length=500, help_text="Texte de l'annonce")
    emoji = models.CharField(max_length=10, blank=True, default="🔥", help_text="Emoji à afficher")
    is_active = models.BooleanField(default=True, help_text="Afficher cette annonce")
    order = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.emoji} {self.text[:50]}..."
