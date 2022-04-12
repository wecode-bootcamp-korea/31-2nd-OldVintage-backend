from django.db import models

from cores.models import TimestampZone

class Product(TimestampZone): 
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    grape    = models.CharField(max_length=100)
    bold     = models.DecimalField(max_digits=3, decimal_places=2)
    tannic   = models.DecimalField(max_digits=3, decimal_places=2)
    sweet    = models.DecimalField(max_digits=3, decimal_places=2)
    acidic   = models.DecimalField(max_digits=3, decimal_places=2)
    winery   = models.ForeignKey('Winery', on_delete=models.CASCADE, related_name='products')
    type     = models.ForeignKey('Type', on_delete=models.CASCADE, related_name='products')
    pairings = models.ManyToManyField('Pairing', through='Productpairing')

    class Meta:
        db_table = 'products'

class Country(TimestampZone):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'countries'
        
class Winery(TimestampZone):
    name        = models.CharField(max_length=100)
    address     = models.CharField(max_length=200)
    latitude    = models.DecimalField(max_digits=10, decimal_places=7)
    longitude   = models.DecimalField(max_digits=10, decimal_places=7)
    description = models.CharField(max_length=1000)
    country     = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='wineries')

    class Meta:
        db_table = 'wineries'

class Type(TimestampZone):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'types'

class Pairing(TimestampZone):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'pairings'

class ProductPairing(TimestampZone):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='productpairings')
    pairing = models.ForeignKey('Pairing', on_delete=models.CASCADE, related_name='productpairings')
    
    class Meta:
        db_table = 'productpairings'