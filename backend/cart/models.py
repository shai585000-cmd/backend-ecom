from django.db import models
from django.conf import settings
from backend.produits.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'

    def __str__(self):
        return f"Panier de {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Article panier'
        verbose_name_plural = 'Articles panier'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} dans le panier de {self.cart.user.username}"
