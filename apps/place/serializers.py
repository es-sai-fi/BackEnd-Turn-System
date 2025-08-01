from rest_framework import serializers
from .models import Place, PlaceCustomUser
from ..service.serializers import ServiceSerializer


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class PlaceGETSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(source='service_id', read_only=True)

    class Meta:
        model = Place
        exclude = ['service_id']
        

class PlaceCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceCustomUser
        fields = '__all__'
