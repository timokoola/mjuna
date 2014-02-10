from django.contrib import admin
admin.autodiscover()


from django.conf.urls import patterns, url, include
from rest_framework.urlpatterns import format_suffix_patterns
from mapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stations', views.StationViewSet)
router.register(r'trains', views.TrainInfoViewSet)
router.register(r'arrivals', views.TrainStationInfoViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')) )