import googlemaps
import urllib.request
import json
from dateutil import parser
#from django.db.models.fields import NullBooleanField
#from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from wBE_app.models import Locations

gmaps = googlemaps.Client(key='') # DO NOT MAKE KEY PUBLIC!
NWS_URL = 'https://api.weather.gov/points/'

@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def searchLocation_API(request):
    if request.method=='GET':
        city_query = request.data['City'].lower()
        state_query = request.data['State'].upper()
        flag = True
        lat = 0, lng = 0 
        for obj in Locations.objects.all():
            if obj.State == state_query or obj.get_State_display.upper() == state_query:
                if obj.City == city_query:
                    lat = str(obj.Latitude)
                    lng = str(obj.Longitude)
                    flag = False
        if flag:
            place_query = city_query + ', ' + state_query
            location = gmaps.geocode(place_query)
            lat = str(round(location[0]['geometry']['location']['lat'],4))
            lng = str(round(location[0]['geometry']['location']['lng'],4))
        points = lat + ',' + lng
        url = NWS_URL + points
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        city = data['properties']['relativeLocation']['properties']['city'].lower()
        state = data['properties']['relativeLocation']['properties']['state'].upper()
        if flag:
            newEntry = Locations(City=city, State=state, Latitude=lat, Longitude=lng)
            if newEntry.is_valid():
                newEntry.save()
        return data['properties']

@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def daily_API(request):
    if request.method=='GET':
        url = searchLocation_API(request)['forecast']
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))

        # for item in data['properties']['periods']:
        #   item.keys()
        # ==>> n items of dict:
        # ==>>  dict_keys(['number', 'name', 'startTime', 'endTime',
        #            'isDaytime', 'temperature', 'temperatureUnit', 
        #            'temperatureTrend', 'windSpeed', 'windDirection', 
        #            'icon', 'shortForecast', 'detailedForecast'])

@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def hourly_API(request):
    if request.method=='GET':
        url = searchLocation_API(request)['forecastHourly']
