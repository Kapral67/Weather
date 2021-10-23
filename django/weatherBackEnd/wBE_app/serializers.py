from rest_framework import serializers
from wBE_app.models import Locations

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Locations
        fields=('City','State','Latitude','Longitude')
