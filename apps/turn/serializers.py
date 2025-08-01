from rest_framework import serializers
from .models import Turn


class CreateTurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = ['owner', 'place_id']


class TurnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turn
        fields = '__all__'
