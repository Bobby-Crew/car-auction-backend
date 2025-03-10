from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarAuctionViewSet

router = DefaultRouter()
router.register(r'auctions', CarAuctionViewSet)

urlpatterns = [
    path('auctions/<int:pk>/bid/', CarAuctionViewSet.as_view({'post': 'bid'}), name='auction-bid'),
    path('', include(router.urls)),
    
] 