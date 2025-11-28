from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from backend.produits.models import Product


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de 1 à 5 étoiles"
    )
    title = models.CharField(max_length=100, blank=True)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']  # Un seul avis par utilisateur par produit
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.user.username} sur {self.product.name} - {self.rating}★"
