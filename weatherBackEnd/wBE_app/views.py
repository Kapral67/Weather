from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

import googlemaps
gmaps = googlemaps.Client(key='') # DO NOT MAKE KEY PUBLIC!
"""
location = gmaps.geocode('Chico, CA')

precise_latitude = location[0]['geometry']['location']['lat']

precise_longitude = location[0]['geometry']['location']['lng']

approx_location = [round(precise_latitude,4),round(precise_longitude,4)] # [lat, long]
"""


# Create your views here.

