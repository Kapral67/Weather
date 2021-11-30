from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Locations(models.Model):
    STATES = [
        # Capital
        ('DC', 'District of Columbia'),

        # States
        ('AL', 'Alabama'),('MT', 'Montana'),('AK', 'Alaska'),('NE', 'Nebraska'),
        ('AZ', 'Arizona'),('NV', 'Nevada'),('AR', 'Arkansas'),('NH', 'New Hampshire'),
        ('CA', 'California'),('NJ', 'New Jersey'),('CO', 'Colorado'),('NM', 'New Mexico'),
        ('CT', 'Connecticut'),('NY', 'New York'),('DE', 'Delaware'),('NC', 'North Carolina'),
        ('FL', 'Florida'),('ND', 'North Dakota'),('GA', 'Georgia'),('OH', 'Ohio'),
        ('HI', 'Hawaii'),('OK', 'Oklahoma'),('ID', 'Idaho'),('OR', 'Oregon'),('IL', 'Illinois'),
        ('PA', 'Pennsylvania'),('IN', 'Indiana'),('RI', 'Rhode Island'),('IA', 'Iowa'),
        ('SC', 'South Carolina'),('KS', 'Kansas'),('SD', 'South Dakota'),('KY', 'Kentucky'),
        ('TN', 'Tennessee'),('LA', 'Louisiana'),('TX', 'Texas'),('ME', 'Maine'),('UT', 'Utah'),
        ('MD', 'Maryland'),('VT', 'Vermont'),('MA', 'Massachusetts'),('VA', 'Virginia'),
        ('MI', 'Michigan'),('WA', 'Washington'),('MN', 'Minnesota'),('WV', 'West Virginia'),
        ('MS', 'Mississippi'),('WI', 'Wisconsin'),('MO', 'Missouri'),('WY', 'Wyoming'),
        
        # Territories
        ('PR', 'Puerto Rico'),
    ]

    City = models.CharField(max_length=64)
    State = models.CharField(choices=STATES, max_length=2)
    Latitude = models.DecimalField(max_digits=6, decimal_places=4)
    Longitude = models.DecimalField(max_digits=7, decimal_places=4)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['City', 'State'], name='Unique City, ST'),
            models.UniqueConstraint(fields=['Latitude', 'Longitude'], name='Unique Location')
        ]

class UserPref(models.Model):
    METRIC = ['Metric', 'US']
    PAGE = ['hourly', 'daily', 'account']
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    measurement = models.CharField(choices=METRIC, max_length=10, blank=True)
    defaultPage = models.CharField(choices=PAGE, max_length=10, blank=True)
