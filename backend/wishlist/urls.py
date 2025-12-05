from django.urls import path
from .views import WishlistView, WishlistAddView, WishlistRemoveView, WishlistCheckView

app_name = 'wishlist'

urlpatterns = [
    path('', WishlistView.as_view(), name='list'),
    path('add/<int:product_id>/', WishlistAddView.as_view(), name='add'),
    path('remove/<int:product_id>/', WishlistRemoveView.as_view(), name='remove'),
    path('check/<int:product_id>/', WishlistCheckView.as_view(), name='check'),
]
