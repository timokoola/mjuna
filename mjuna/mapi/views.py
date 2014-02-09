from mapi.models import Station
from mapi.serializers import StationSerializer
from rest_framework import generics


class StationList(generics.ListCreateAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class StationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer