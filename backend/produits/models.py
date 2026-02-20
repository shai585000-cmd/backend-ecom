from django.db import models
from backend.home.models import Category
from backend.users.models import User


class Brand(models.Model):
    """Marques de téléphones"""
    name = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Neuf'),
        ('refurbished', 'Reconditionné'),
        ('used', 'Occasion'),
    ]

    NETWORK_CHOICES = [
        ('2g', '2G'),
        ('3g', '3G'),
        ('4g', '4G'),
        ('5g', '5G'),
    ]

    OS_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
        ('other', 'Autre'),
    ]

    # Champs de base
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promotion = models.BooleanField(default=False)
    promotion_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)

    # Champs spécifiques téléphones
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    model_name = models.CharField(max_length=100, blank=True, verbose_name="Modèle")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='new', verbose_name="État")
    color = models.CharField(max_length=50, blank=True, verbose_name="Couleur")
    
    # Spécifications techniques
    ram = models.PositiveIntegerField(blank=True, null=True, help_text="RAM en Go")
    storage = models.PositiveIntegerField(blank=True, null=True, help_text="Stockage en Go")
    screen_size = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="Taille écran en pouces")
    battery_capacity = models.PositiveIntegerField(blank=True, null=True, help_text="Capacité batterie en mAh")
    operating_system = models.CharField(max_length=20, choices=OS_CHOICES, blank=True, verbose_name="Système d'exploitation")
    network = models.CharField(max_length=10, choices=NETWORK_CHOICES, blank=True, verbose_name="Réseau")
    dual_sim = models.BooleanField(default=False, verbose_name="Double SIM")
    
    # Caméra
    main_camera = models.CharField(max_length=50, blank=True, help_text="Ex: 108MP + 12MP + 5MP")
    front_camera = models.CharField(max_length=50, blank=True, help_text="Ex: 32MP")

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Retourne le prix final (promo ou normal)"""
        if self.promotion and self.promotion_price:
            return self.promotion_price
        return self.price

    @property
    def discount_percentage(self):
        """Calcule le pourcentage de réduction"""
        if self.promotion and self.promotion_price and self.price > 0:
            return int(((self.price - self.promotion_price) / self.price) * 100)
        return 0
