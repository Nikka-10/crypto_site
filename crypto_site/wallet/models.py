from django.db import models

class Crypto(models.Model):
    name = models.CharField(max_length=150,  unique=True)
    symbol = models.CharField(max_length=150,  unique=True)
    price_usd = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    

