from django.urls import path

from . import views

urlpatterns = [
    path('daily', views.daily_API, name = 'daily'),
    path('hourly', views.hourly_API, name = 'hourly'),
]