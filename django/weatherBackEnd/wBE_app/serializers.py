from rest_framework import serializers
from wBE_app.models import Locations, UserPref
#from django.contrib.auth.models import User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('City','State','Latitude','Longitude')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        fields = ('id', 'username', 'email', 'measurement', 'defaultPage')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPref
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserPref.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
