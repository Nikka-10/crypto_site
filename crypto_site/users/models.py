from django.db import models

class user(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    mail = models.CharField(max_length=150, unique=True) 
    password = models.CharField(max_length=150)