from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

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
        # ('PR', 'Puerto Rico'),
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

class AccountManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )

        return self._create_user(email, password, **extra_fields)

class Account(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = None
    METRIC = [('SI', 'SI'), ('US', 'US'), ('Default', 'Default')]
    measurement = models.CharField(choices=METRIC, max_length=16, blank=True)
    PAGE = [('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Account', 'Account'), ('Default', 'Default')]
    defaultPage = models.CharField(choices=PAGE, max_length=16, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AccountManager()
