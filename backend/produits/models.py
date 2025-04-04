from django.db import models
from backend.home.models import Category
from backend.users.models import User

class Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Le champ image
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
    stock = models.CharField(max_length=255, default=0)

    def __str__(self):
        return self.name
