from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),  # /api/cart/
    path('cart/items/', views.CartItemView.as_view(), name='cart-items'),  # /api/cart/items/
    path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),  # /api/cart/checkout/
]