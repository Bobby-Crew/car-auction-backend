from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import CarAuction, CarImage
from .serializers import CarAuctionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class CarAuctionViewSet(viewsets.ModelViewSet):
    queryset = CarAuction.objects.all()
    serializer_class = CarAuctionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = CarAuction.objects.all()
        if self.action == 'list':
            if 'my_auctions' in self.request.query_params:
                return queryset.filter(seller=self.request.user)
            elif not self.request.user.is_authenticated and 'featured' in self.request.query_params:
                # Return only 4 random auctions for non-authenticated users on home page
                return queryset.order_by('?')[:4]
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=True, methods=['post'])
    def images(self, request, pk=None):
        auction = self.get_object()
        images = request.FILES.getlist('images')
        is_primary_values = request.POST.getlist('is_primary')

        try:
            for image, is_primary in zip(images, is_primary_values):
                CarImage.objects.create(
                    auction=auction,
                    image=image,
                    is_primary=is_primary.lower() == 'true'
                )
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error uploading images: {str(e)}")
            return Response(
                {"error": "Failed to upload images"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def bid(self, request, pk=None):
        auction = self.get_object()
        bid_amount = request.data.get('bid_amount')

        if auction.place_bid(bid_amount):
            return Response({"message": "Bid placed successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Bid must be higher than the current bid or auction has ended."}, status=status.HTTP_400_BAD_REQUEST)
