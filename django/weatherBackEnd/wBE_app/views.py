import googlemaps
import urllib.request
import json
import string
from dateutil import parser # TimeZone handling

#from django.db.models.fields import NullBooleanField
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import login

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from wBE_app.serializers import LocationSerializer, UserSerializer, RegisterSerializer
from wBE_app.models import Locations

gmaps = googlemaps.Client(key = '') # DO NOT MAKE KEY PUBLIC!
NWS_URL = 'https://api.weather.gov/points/'

@csrf_exempt
#@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def searchLocation_API(request):
    #if request.method=='GET':
    city_query = string.capwords(request.data['City'])
    state_query = request.data['State'].upper()
    flag = True
    lat = 0
    lng = 0 
    for obj in Locations.objects.all():
        if obj.State == state_query or obj.get_State_display().upper() == state_query:
            if obj.City == city_query:
                lat = round(obj.Latitude,4)
                lng = round(obj.Longitude,4)
                flag = False
                break
    if flag:
        place_query = city_query + ', ' + state_query
        location = gmaps.geocode(place_query)
        lat = round(location[0]['geometry']['location']['lat'],4)
        lng = round(location[0]['geometry']['location']['lng'],4)
    points = str(lat) + ',' + str(lng)
    url = NWS_URL + points
    response = urllib.request.urlopen(url)
    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))
    if flag:
        flags = [False, False]
        for c in location[0]['address_components']:
            if c['types'][0] == 'locality':
                city = string.capwords(c['long_name'])
                flags[0] = True
            elif c['types'][0] == 'administrative_area_level_1':
                state = c['short_name'].upper()
                flags[1] = True
            if flags[0] and flags[1]:
                break
        #city = data['properties']['relativeLocation']['properties']['city'].lower()
        #state = data['properties']['relativeLocation']['properties']['state'].upper()
        #lat = round(data['properties']['relativeLocation']['geometry']['coordinates'][1],4)
        #lng = round(data['properties']['relativeLocation']['geometry']['coordinates'][0],4)
        newEntry = {'City':city, 'State':state, 'Latitude':lat, 'Longitude':lng}
        newEntry_serializer = LocationSerializer(data = newEntry)
        if newEntry_serializer.is_valid(raise_exception = True):
            newEntry_serializer.save()
            #return JsonResponse("Updated Successfully",safe=False)
    return data['properties']

# for item in data['properties']['periods']:
#   item.keys()
# ==>> n items of dict:
# ==>> dict_keys(['number', 'name', 'startTime', 'endTime',
#            'isDaytime', 'temperature', 'temperatureUnit', 
#            'temperatureTrend', 'windSpeed', 'windDirection', 
#            'icon', 'shortForecast', 'detailedForecast'])

@csrf_exempt
@api_view(['GET', 'POST'])
#@api_view(['GET', 'PUT'])
@parser_classes([JSONParser])
def daily_API(request):
    if request.method == 'POST':
        url = searchLocation_API(request)['forecast']
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        return JsonResponse(data['properties'], safe = False)
    elif request.method == 'GET':
        locations = Locations.objects.all()
        location_serializer = LocationSerializer(locations, many = True)
        return JsonResponse(location_serializer.data, safe = False)

@csrf_exempt
@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def hourly_API(request):
    if request.method == 'POST':
        url = searchLocation_API(request)['forecastHourly']
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        return JsonResponse(data['properties'], safe = False)
    elif request.method == 'GET':
        locations = Locations.objects.all()
        location_serializer = LocationSerializer(locations, many = True)
        return JsonResponse(location_serializer.data, safe = False)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context = self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format = None):
        serializer = AuthTokenSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format = None)
            
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
