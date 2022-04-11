from django.db import models

from cores.models import TimestampZone

class Review(TimestampZone): 
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, related_name='reviews')
    user    = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='reviews')
    rating  = models.IntegerField()
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = 'reviews'
        
class Image(TimestampZone): 
    image_url = models.CharField(max_length=1000)
    review    = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'images'