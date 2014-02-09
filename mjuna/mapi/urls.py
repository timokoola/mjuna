from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from mapi import views

urlpatterns = patterns('',
    url(r'^stations/$', views.StationList.as_view()),
    url(r'^stations/(?P<pk>[0-9]+)/$', views.StationDetail.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)