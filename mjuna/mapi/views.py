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


class RunningTrainViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = RunningTrain.objects.all()
    serializer_class = RunningTrainSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class RunningTrainStopInfoViewSet(viewsets.ModelViewSet):

    """Information of a particular train as in relation
    to a particular station"""
    queryset = RunningTrainStopInfo.objects.all()
    serializer_class = RunningTrainStopInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
