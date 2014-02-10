from mapi.models import *
from django.forms import widgets
from rest_framework import serializers


class StationSerializer(serializers.HyperlinkedModelSerializer):

    """Serializer for Station objects"""
    class Meta:
        model = Station
        fields = ('url', 'title', 'code', 'latitude', 'longitude', 'timestamp')


class TrainInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrainInfo
        fields = (
            'url', 'category', 'title', 'latitude', 'longitude', 'from_station',
            'to_station', 'status', 'heading', 'train_type', 'reason_code', 'timestamp')

class TrainStationInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TrainStationInfo
        fields = (
            'train','guid','title','scheduledTime','scheduledDepartTime','eta','etd','station','completed','status','lateness','timestamp')
