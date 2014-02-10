from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import link
from rest_framework.response import Response

from mapi.models import *
from mapi.serializers import *
from mapi.permissions import *
from rest_framework import viewsets

from rest_framework.decorators import link


class StationViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class TrainInfoViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = TrainInfo.objects.all()
    serializer_class = TrainInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class TrainStationInfoViewSet(viewsets.ModelViewSet):

    """Information of a particular train as in relation
    to a particular station"""
    queryset = TrainStationInfo.objects.all()
    serializer_class = TrainStationInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
