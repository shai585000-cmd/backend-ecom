from django.db import models
from django.conf import settings


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    neighborhood = models.CharField(max_length=100, blank=True)  # Quartier
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Cameroun')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Shipping addresses"
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.address}"

    def save(self, *args, **kwargs):
        # Si cette adresse est définie comme par défaut, retirer le défaut des autres
        if self.is_default:
            ShippingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class ShippingZone(models.Model):
    name = models.CharField(max_length=100)  # Ex: Douala, Yaoundé, etc.
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.shipping_fee} FCFA"
