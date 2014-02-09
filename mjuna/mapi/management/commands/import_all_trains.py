from django.core.management.base import BaseCommand, CommandError
from mapi.models import *
import feedparser
from mjuna.settings import TRAIN_FEED_URL
import datetime
import urllib

class Command(BaseCommand):
    help = 'Imports all trains moving and stores them to database (mostly for testing)'
    d = feedparser.parse(TRAIN_FEED_URL)
    print "There are %d trains running." % (len(d.entries))
    for de in d.entries:
        try:
            ti = TrainInfo.objects.get(guid=de.guid.split("/")[-1])
        except: 
            ti = TrainInfo()
            ti.guid = de.guid.split("/")[-1]
        try:
            ti.category = de.get("category","1")
            ti.title = de.title
            geoco = de.georss_point.split()
            print geoco
            ti.latitude = geoco[0] if geoco[0] else Decimal(0.0)
            ti.longitude = geoco[1] if geoco[1] else Decimal(0.0)
            print "%s -> %s" % (de["from"],de["to"])
            ti.from_station = Station.objects.get(code=urllib.quote(de["from"]))
            ti.to_station = Station.objects.get(code=urllib.quote(de["to"]))
            ti.status = de.status
            ti.heading = de.dir if de.dir else -1
            ti.train_type = de.cat
            ti.timestamp = datetime.datetime.now()
            ti.save()
        except KeyError:
            continue
