from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
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

# class UserPref(models.Model):
#     METRIC = [('SI', 'Metric'), ('US', 'Customary')]
#     PAGE = [('Hour', 'hourly'), ('Day', 'daily'), ('User', 'account')]
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     measurement = models.CharField(choices=METRIC, max_length=10, blank=True)
#     defaultPage = models.CharField(choices=PAGE, max_length=10, blank=True)

class AccountManager(BaseUserManager):
    # def _create_user(self, email, password=None):
    #     if not email:
    #         raise ValueError("Email Address is Required.")
    #     user = self.model(
    #         email=self.normalize_email(email),
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user
    # def create_superuser(self, email, password):
    #     user = self.create_user(
    #         email=self.normalize_email(email),
    #         password=password,
    #     )
    #     user.is_admin=True
    #     user.is_staff=True
    #     user.is_superuser=True
    #     user.save(using=self._db)
    #     return user

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
    # date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    METRIC = [('SI', 'SI'), ('US', 'US'), ('Default', 'Default')]
    measurement = models.CharField(choices=METRIC, max_length=16, blank=True)
    PAGE = [('Hourly', 'Hourly'), ('Daily', 'Daily'), ('Account', 'Account'), ('Default', 'Default')]
    defaultPage = models.CharField(choices=PAGE, max_length=16, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AccountManager()
