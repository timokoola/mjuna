# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from mapi.models import *
import feedparser
from mjuna.settings import STATION_FEED_URL
import django.utils.timezone
import urllib

STATIONS = [
    "ALV", "DRA", "EPZ", "ENO", "EPO", "HPJ", "HPK", "HAA", "HKS", "HNK", "HKP", "HVA", "HAU", "HNV", "HKI","HR", "HKH","HK","HP", "HPL","HY","HL", u"H%C3%96L", "ILM", "ITA", "ILA", "IMR", "IKR", "IKO", "IKY", "JNS","JK", "JRS", "JTS","JJ","JY", u"J%C3%84S","JR","JP", "KAJ", "KAN", "KNS","KR", "KRU", "KHA", "KLH", "KNI","KA", "KEM", u"KJ%C3%84", "KEA","KE", u"KI%C3%84", "KTI", "KEU", "KIL", "KKN", "KIT", "KRV", "KOH", "KVH", "KVY", "KKI", "KOK", "KLI", "KLO", "KON", "KRA", "KRS", "KTA", "KTS","KV", "KUO", "KUT", "KYN","KY", "KLN", u"KR%C3%96", u"K%C3%84P","LH", "LAI", "LNA","LR", "LAA", "LPO", "LPA", u"LP%C3%84", "LPV", "LIS", "LVT","LM", "LOH", "LMA", "LUS","ML", "MLO", "MNK",
    "MRL", "MAS","MI", "MLA","MH", "MUL", "MKI","MY", "MYR", u"M%C3%84K", u"ML%C3%84","MR", "NSL", "NVL", "NOA", "NUP", "NRM","OI","OV", "OVK","OU","OL", "OLK", "PTI", "PTO", "PAR", "PKO", "PRL", "PSL", "PEL", "PVI","PM", "PTS","PH", "PJM", "POH", "PRI", "PLA", "PMK", "PUN", "PUR", u"PH%C3%84", u"PN%C3%84", "PKY", "RKL", "REE","RI", "ROI", "RNN", "RKI","RY", "SLO", "STA", "SAU", "SAV","SL","SK", "SIJ", "SPL", "STI", "SKY", "SKV", "SNJ", "TMS", "TPE", "TNA", "TSL","TK", "TRV", "TKL","TL", "TOL", "TOR", "TRL","TU", "TKU", "TUS", "TUU", "UIM", "UTJ", u"UK%C3%84", "VAA","VS", "VNA", "VMO", "VMA", "VKS", "VAR", "VTI", "VIH", "VIA", "VNJ", "VLP", "VLH", "VSL", "YST", "YTR","YV", u"%C3%84HT"]


class Command(BaseCommand):
    help = 'Imports all stations and stores them to database'

    def handle(self, *args, **options):
        for i in STATIONS:
            print len(STATIONS)
            d = feedparser.parse(STATION_FEED_URL + i)
            if not d.has_key("bozo_exception"):
                s = Station()
                try:
                    s.title = d.feed.title
                    s.code = i
                    geoco = d.feed[u'georss_point'].split()
                    s.latitude = geoco[0]
                    s.longitude = geoco[1]
                    s.timestamp = django.utils.timezone.now()
                    s.save()
                except KeyError:
                    print "Error for %s" % i
            else:
                print d["bozo_exception"]

