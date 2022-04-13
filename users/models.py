from django.db import models

from cores.models import TimestampZone

class User(TimestampZone): 
    email      = models.CharField(max_length=100, unique=True)
    name       = models.CharField(max_length=100, null=True)
    kakao_id   = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'users'
        
class Wishlist(TimestampZone): 
    product = models.ForeignKey('products.product', on_delete=models.CASCADE, related_name='wishlists')
    user    = models.ForeignKey('users.user', on_delete=models.CASCADE, related_name='wishlists')
    
    class Meta:
        db_table = 'wishlists'