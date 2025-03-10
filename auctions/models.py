from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CarAuction(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    buy_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField(default=timezone.now)
    duration_hours = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def end_time(self):
        return self.start_time + timezone.timedelta(hours=self.duration_hours)
    
    @property
    def time_left(self):
        if timezone.now() > self.end_time:
            return "Auction ended"
        
        time_remaining = self.end_time - timezone.now()
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = (time_remaining.seconds % 3600) // 60
        
        if days > 0:
            return f"{days} days"
        elif hours > 0:
            return f"{hours} hours"
        else:
            return f"{minutes} minutes"
        

    def place_bid(self, bid_amount):
        if timezone.now() < self.end_time:
            if bid_amount > self.current_bid:
                self.current_bid = bid_amount
                self.save()
                return True
        return False

class CarImage(models.Model):
    auction = models.ForeignKey(CarAuction, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)