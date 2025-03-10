from rest_framework import serializers
from .models import CarAuction, CarImage
from django.contrib.auth.models import User

class CarImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CarImage
        fields = ['id', 'image', 'is_primary']
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
        return None

class CarAuctionSerializer(serializers.ModelSerializer):
    images = CarImageSerializer(many=True, read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)
    time_left = serializers.CharField(read_only=True)

    class Meta:
        model = CarAuction
        fields = [
            'id', 
            'name', 
            'year', 
            'current_bid', 
            'starting_bid',
            'buy_now_price', 
            'start_time', 
            'duration_hours',
            'time_left',
            'seller_username',
            'images'
        ] 