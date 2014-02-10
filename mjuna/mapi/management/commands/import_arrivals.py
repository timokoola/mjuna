# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from mapi.models import *
import feedparser
from mjuna.settings import STATION_FEED_URL
import django.utils.timezone
import urllib


class Command(BaseCommand):
    args = '<traing guid>'
    help = 'Imports all stations and stores them to database'

    def handle(self, *args, **options):
        if args:
            print "Hello continue here %s" % ",".join(args)
        else:
            print "Hello"
