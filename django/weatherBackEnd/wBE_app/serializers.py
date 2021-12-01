from rest_framework import serializers
from wBE_app.models import Locations, Account

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ('City','State','Latitude','Longitude')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'measurement', 'defaultPage']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'measurement', 'defaultPage', 'password']
        extra_kwargs = {"password": {"write_only": True}}
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = Account
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required = True)

class AlterPrefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('measurement', 'defaultPage')
