from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingAddressViewSet, ShippingZoneViewSet

app_name = 'shipping'

router = DefaultRouter()
router.register(r'addresses', ShippingAddressViewSet, basename='address')
router.register(r'zones', ShippingZoneViewSet, basename='zone')

urlpatterns = [
    path('', include(router.urls)),
]
