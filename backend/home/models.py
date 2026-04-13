from django.db import models

# Create your models here.


class HeroSection(models.Model):
    """Section hero de la page d'accueil - modifiable depuis l'admin"""
    badge_text = models.CharField(max_length=100, default="Nouveautés 2024", help_text="Texte du badge (ex: Nouveautés 2024)")
    title = models.CharField(max_length=255, default="Découvrez les meilleurs smartphones du marché")
    title_highlight = models.CharField(max_length=100, blank=True, default="smartphones", help_text="Mot mis en rouge dans le titre")
    description = models.TextField(default="iPhone 15, Samsung Galaxy S24, et bien plus encore. Livraison gratuite et garantie 12 mois.")
    button1_text = models.CharField(max_length=100, default="Explorer les produits")
    button1_link = models.CharField(max_length=200, default="/produit")
    button2_text = models.CharField(max_length=100, default="Voir les promos")
    button2_link = models.CharField(max_length=200, default="/produit?promo=true")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Section Hero'
        verbose_name_plural = 'Sections Hero'

    def __str__(self):
        return self.title


class FeatureItem(models.Model):
    """Icônes de fonctionnalités (Livraison, Garantie, Support, Paiement)"""
    ICON_CHOICES = [
        ('truck', 'Livraison'),
        ('shield', 'Garantie'),
        ('headphones', 'Support'),
        ('credit-card', 'Paiement'),
        ('gift', 'Cadeau'),
        ('star', 'Étoile'),
    ]
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default='truck')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Fonctionnalité'
        verbose_name_plural = 'Fonctionnalités'

    def __str__(self):
        return self.title


class SolutionCard(models.Model):
    """Cartes de solutions/catégories sur la page d'accueil"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, default='smartphone', help_text="Nom de l'icône (smartphone, headphones, monitor, flame)")
    link = models.CharField(max_length=200, default="/produit")
    bg_gradient = models.CharField(max_length=100, default="from-gray-800 to-gray-900", help_text="Classes Tailwind du dégradé")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Carte Solution'
        verbose_name_plural = 'Cartes Solutions'

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Banniere'
        verbose_name_plural = 'Bannieres'

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

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
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'

    def __str__(self):
        return f"{self.emoji} {self.text[:50]}..."
