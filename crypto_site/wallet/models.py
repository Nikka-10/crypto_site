from django.db import models
from users.models import CustomUser

class Crypto(models.Model):
    name = models.CharField(max_length=150,  unique=True)
    symbol = models.CharField(max_length=150,  unique=True)
    price_usd = models.DecimalField(max_digits=12,decimal_places=2, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Wallet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=0)
