from django.db import models

# Create your models here.

class Locations(models.Model):
    City = models.CharField(max_length=64)
    State = models.CharField(max_length=2)
    Latitude = models.DecimalField(max_digits=6, decimal_places=4)
    Longitude = models.DecimalField(max_digits=7, decimal_places=4)
    