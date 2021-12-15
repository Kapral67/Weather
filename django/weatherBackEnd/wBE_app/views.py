from django.views.decorators import csrf
import googlemaps
import urllib.request
import json
import string
from dateutil import parser # TimeZone handling

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import login
from django.utils.decorators import method_decorator

from rest_framework import generics, permissions, status, mixins
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken

from rest_auth.registration.views import RegisterView

from wBE_app.serializers import AlterPrefsSerializer, LocationSerializer, UserSerializer, RegisterSerializer, ChangePasswordSerializer
from wBE_app.models import Locations, Account

with open('/code/django/weatherBackEnd/wBE_app/secret/geocode.txt') as f:
    API_KEY = f.read().strip()

gmaps = googlemaps.Client(key = API_KEY) # DO NOT MAKE KEY PUBLIC!
NWS_URL = 'https://api.weather.gov/points/'
ALERT_URL = 'https://api.weather.gov/alerts/active?point='

@parser_classes([JSONParser])
@csrf_exempt
def searchLocation_API(request, alert = False):
    city_query = string.capwords(request.data['City'])
    state_query = request.data['State'].upper()
    if((city_query == "New York City" or city_query == "Nyc") and (state_query == "NY" or state_query == "NEW YORK")):
        city_query = "New York"
    elif((city_query == "La") and (state_query == "CA" or state_query == "CALIFORNIA")):
        city_query = "Los Angeles"
    elif((city_query == "Saint Louis" or city_query == "St Louis") and (state_query == "MO" or state_query == "MISSOURI")):
        city_query = "St. Louis"
    elif((city_query == "St. Paul" or city_query == "St Paul") and (state_query == "MN" or state_query == "MINNESOTA")):
        city_query = "Saint Paul"
    elif((city_query == "Tahoe" or city_query == "Lake Tahoe") and (state_query == "CA" or state_query == "CALIFORNIA")):
        city_query = "Tahoe City"
    elif((city_query == "Tahoe" or city_query == "Lake Tahoe") and (state_query == "NV" or state_query == "NEVADA")):
        city_query = "Incline Village"
    elif((city_query == "Death Valley") and (state_query == "CA" or state_query == "CALIFORNIA")):
        city_query = "Furnace Creek"
    elif((city_query == "Staten Island" or city_query == "Brooklyn" or city_query == "Queens" or city_query == "Bronx" or city_query == "Manhattan") and (state_query == "NY" or "NEW YORK")):
        city_query = "New York"
    elif((city_query == "Redwood" or city_query == "Rwc") and (state_query == "CA" or "CALIFORNIA")):
        city_query = "Redwood City"
    flag = True
    lat = 0
    lng = 0 
    for obj in Locations.objects.all():
        if obj.State == state_query or obj.get_State_display().upper() == state_query:
            if obj.City == city_query:
                lat = round(obj.Latitude,4)
                lng = round(obj.Longitude,4)
                city = obj.City
                state = obj.State
                flag = False
                break
    if flag:
        place_query = city_query + ', ' + state_query
        try:
            location = gmaps.geocode(place_query)
            lat = round(location[0]['geometry']['location']['lat'],4)
            lng = round(location[0]['geometry']['location']['lng'],4)
        except:
            return 502
    points = str(lat) + ',' + str(lng)
    if alert:
        return points
    url = NWS_URL + points
    try:
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
    except:
        return 502
    if flag:
        flags = [False, False]
        city = None
        state = None
        full_state = None
        for c in location[0]['address_components']:
            if c['types'][0] == 'locality':
                city = string.capwords(c['long_name'])
                flags[0] = True
            elif c['types'][0] == 'administrative_area_level_1':
                state = c['short_name'].upper()
                full_state = c['long_name'].upper()
                flags[1] = True
            if flags[0] and flags[1]:
                break
        if city != None and city != "" and state != None and state != "" and lat != 0 and lng != 0 and full_state != None and full_state != "" and (state == state_query or full_state == state_query):
            newEntry = {'City':city, 'State':state, 'Latitude':lat, 'Longitude':lng}
            newEntry_serializer = LocationSerializer(data = newEntry)
            if newEntry_serializer.is_valid(raise_exception = False):
                newEntry_serializer.save()
    if city == None or city == "":
        city = city_query
    if state == None or state == "":
        state = state_query
    if state != state_query:
        return [data['properties'], [city, state], True]
    else:
        return [data['properties'], [city, state], False]

@api_view(['POST'])
@parser_classes([JSONParser])
@csrf_exempt
def alert_API(request):
    if request.method == 'POST':
        points = searchLocation_API(request, alert = True)
        if points == 502:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        url = ALERT_URL + points
        try:
            response = urllib.request.urlopen(url)
            encoding = response.info().get_content_charset('utf8')
            data = json.loads(response.read().decode(encoding))
        except:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        if data['features'] != []:
            obj = []
            for d in data['features']:
                try:
                    head = d['properties']['headline']
                except:
                    head = None
                try:
                    desc = d['properties']['description']
                except:
                    desc = ""
                try:
                    sev = d['properties']['severity']
                except:
                    sev = "Unknown"
                if head != None and head != "":
                    obj.append([head, desc, sev])
            if obj != [[]] and obj != []:
                return JsonResponse(obj, safe = False)
            else:
                return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        else:
            return Response(None, status = status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@csrf_exempt
def daily_API(request):
    if request.method == 'POST':
        api = searchLocation_API(request)
        if api == 502:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        url = api[0]['forecast']
        try:
            response = urllib.request.urlopen(url)
            encoding = response.info().get_content_charset('utf8')
            data = json.loads(response.read().decode(encoding))
        except:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        return JsonResponse({"weather": data['properties'], "city": api[1][0], "state": api[1][1], "updateState": api[2]}, safe = False)
    elif request.method == 'GET':
        locations = Locations.objects.all()
        location_serializer = LocationSerializer(locations, many = True)
        return JsonResponse(location_serializer.data, safe = False)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@csrf_exempt
def hourly_API(request):
    if request.method == 'POST':
        whether = searchLocation_API(request)
        if whether == 502:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        url = whether[0]['forecastHourly']
        try:
            response = urllib.request.urlopen(url)
            encoding = response.info().get_content_charset('utf8')
            data = json.loads(response.read().decode(encoding))
        except:
            return Response(None, status = status.HTTP_502_BAD_GATEWAY)
        weather = data['properties']
        weather.update({"timeZone": whether[0]['timeZone']})
        return JsonResponse({"weather": weather, "city": whether[1][0], "state": whether[1][1], "updateState": whether[2]}, safe = False)
    elif request.method == 'GET':
        locations = Locations.objects.all()
        location_serializer = LocationSerializer(locations, many = True)
        return JsonResponse(location_serializer.data, safe = False)

class GenericUserAPI(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser,]
    serializer_class = UserSerializer
    queryset = Account.objects.all()

    lookup_field = 'id'
    @method_decorator(csrf_exempt)
    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)
    @method_decorator(csrf_exempt)
    def put(self, request):
        return self.update(request, id)
    @method_decorator(csrf_exempt)
    def delete(self, request, id):
        return self.destroy(request, id)

class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = False):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status = status.HTTP_418_IM_A_TEAPOT)

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    @method_decorator(csrf_exempt)
    def post(self, request, format = None):
        serializer = AuthTokenSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            user = serializer.validated_data['user']
            login(request, user)
            return super(LoginAPI, self).post(request, format = None)
          
class UserAPI(generics.RetrieveAPIView, mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    @method_decorator(csrf_exempt)
    def get_object(self):
        return self.request.user
    @method_decorator(csrf_exempt)
    def delete(self, request):
        return self.destroy(self.request.user)

class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = [permissions.IsAuthenticated,]
    @method_decorator(csrf_exempt)
    def get_object(self, queryset = None):
        obj = self.request.user
        return obj
    @method_decorator(csrf_exempt)
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                    status = 420)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_202_ACCEPTED,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class AlterPrefsAPI(generics.UpdateAPIView):
    serializer_class = AlterPrefsSerializer
    model = Account
    permission_classes = [permissions.IsAuthenticated,]
    @method_decorator(csrf_exempt)
    def get_object(self, queryset = None):
        obj = self.request.user
        return obj
    @method_decorator(csrf_exempt)
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data = request.data, partial = True)
        if serializer.is_valid():
            ut = serializer.data.get('measurement')
            pg = serializer.data.get('defaultPage')
            self.object.measurement = ut
            self.object.defaultPage = pg
            self.object.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
