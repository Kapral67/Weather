from django.views.decorators import csrf
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

#@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@csrf_exempt
def searchLocation_API(request):
    #if request.method=='GET':
    city_query = string.capwords(request.data['City'])
    if(city_query == "New York City" or city_query == "Nyc"):
        city_query = "New York"
    elif(city_query == "La"):
        city_query = "Los Angeles"
    else:
        city_query = city_query.replace("St.", "Saint")
    state_query = request.data['State'].upper()
    # if(len(state_query) > 2):
    #     state_query = state_query.title()
    # test_query = {'City':city_query, 'State':state_query, 'Latitude':0, 'Longitude':0}
    # tmp_serializer = LocationSerializer(data = test_query)
    # if tmp_serializer.is_valid(raise_exception = True):
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

@api_view(['GET', 'POST'])
#@api_view(['GET', 'PUT'])
@parser_classes([JSONParser])
@csrf_exempt
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

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@csrf_exempt
def hourly_API(request):
    if request.method == 'POST':
        whether = searchLocation_API(request)
        url = whether['forecastHourly']
        response = urllib.request.urlopen(url)
        encoding = response.info().get_content_charset('utf8')
        data = json.loads(response.read().decode(encoding))
        weather = data['properties']
        weather.update({"timeZone": whether['timeZone']})
        return JsonResponse(weather, safe = False)
    elif request.method == 'GET':
        locations = Locations.objects.all()
        location_serializer = LocationSerializer(locations, many = True)
        return JsonResponse(location_serializer.data, safe = False)

# class RegisterAPI(RegisterView):
#     queryset = User.objects.all()

# class UserAPI(APIView):
#     @staticmethod
#     def get(request):
#         users = Account.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

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

    # def post(self, request):
    #     return self.create(request)
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
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_202_ACCEPTED)
            # return Response({
            #     "user": UserSerializer(user, context = self.get_serializer_context()).data,
            #     "token": AuthToken.objects.create(user)[1]
            # })
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
          
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    @method_decorator(csrf_exempt)
    def get_object(self):
        return self.request.user

# class PreferencesAPI(generics.RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated,]
#     serializer_class = PreferencesSerializer
#     def get_object(self):
#         return self.request.user

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
            # else:
            #     return Response(status = status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
