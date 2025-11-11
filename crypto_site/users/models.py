from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    has_2FA = models.BooleanField(default=False)
    
    