from mapi.models import *
from django.forms import widgets
from rest_framework import serializers


class StationSerializer(serializers.ModelSerializer):

    """Serializer for Station objects"""
    class Meta:
        model = Station
        fields = ('id', 'title', 'code', 'latitude', 'longitude', 'timestamp')


class TrainInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainInfo
        fields = (
            'id', 'category', 'title', 'latitude', 'longitude', 'from_station',
            'to_station', 'status', 'heading', 'train_type', 'reason_code', 'timestamp')
