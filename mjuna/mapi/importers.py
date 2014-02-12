from mapi.models import *
from mapi.models import *
import feedparser
import django.utils.timezone
import urllib
from mjuna.settings import STATION_FEED_URL, TRAIN_FEED_URL, TRAIN_DATA_URL
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

STATIONS = [
    "ALV", "DRA", "EPZ", "ENO", "EPO", "HPJ", "HPK", "HAA",
    "HKS", "HNK", "HKP", "HVA",
    "HAU", "HNV", u"HKI", "HR", "HKH", "HK", "HP", "HPL", "HY", "HL",
    u"H%C3%96L", "ILM", "ITA", "ILA", "IMR", "IKR", "IKO", "IKY", "JNS",
    "JK", "JRS", "JTS", "JJ", "JY", u"J%C3%84S", "JR", "JP", "KAJ", "KAN",
    "KNS", "KR", "KRU", "KHA", "KLH", "KNI", "KA", "KEM", u"KJ%C3%84",
    "KEA", "KE", u"KI%C3%84", "KTI", "KEU", "KIL", "KKN", "KIT", "KRV",
    "KOH", "KVH", "KVY", "KKI", "KOK", "KLI", "KLO", "KON", "KRA", "KRS",
    "KTA", "KTS", "KV", "KUO", "KUT", "KYN", "KY", "KLN", u"KR%C3%96",
    u"K%C3%84P", "LH", "LAI", "LNA", "LR", "LAA", "LPO", "LPA", u"LP%C3%84",
    "LPV", "LIS", "LVT", "LM", "LOH", "LMA", "LUS", "ML", "MLO", "MNK",
    "MRL", "MAS", "MI", "MLA", "MH", "MUL", "MKI", "MY", "MYR", u"M%C3%84K",
    u"ML%C3%84", "MR", "NSL", "NVL", "NOA", "NUP", "NRM", "OI", "OV", "OVK",
    "OU", "OL", "OLK", "PTI", "PTO", "PAR", "PKO", "PRL", "PSL", "PEL",
    "PVI", "PM", "PTS", "PH", "PJM", "POH", "PRI", "PLA", "PMK", "PUN",
    "PUR", u"PH%C3%84", u"PN%C3%84", "PKY", "RKL", "REE", "RI", "ROI",
    "RNN", "RKI", "RY", "SLO", "STA", "SAU", "SAV", "SL", "SK", "SIJ",
    "SPL", "STI", "SKY", "SKV", "SNJ", "TMS", "TPE", "TNA", "TSL", "TK",
    "TRV", "TKL", "TL", "TOL", "TOR", "TRL", "TU", "TKU", "TUS", "TUU",
    "UIM", "UTJ", u"UK%C3%84", "VAA", "VS", "VNA", "VMO", "VMA", "VKS",
    "VAR", "VTI", "VIH", "VIA", "VNJ", "VLP", "VLH", "VSL", "YST",
    "YTR", "YV", u"%C3%84HT"]


def import_all_trains():
    d = feedparser.parse(TRAIN_FEED_URL)
    print "There are %d trains running." % (len(d.entries))
    for de in d.entries:
        try:
            ti = RunningTrain.objects.get(guid=de.guid.split("/")[-1])
        except:
            ti = RunningTrain()
            ti.guid = de.guid.split("/")[-1]
        try:
            ti.category = de.get("category", "1")
            ti.title = de.title
            geoco = de.georss_point.split()
            print geoco
            ti.latitude = geoco[0] if geoco[0] else Decimal(0.0)
            ti.longitude = geoco[1] if geoco[1] else Decimal(0.0)
            print "%s -> %s" % (de["from"], de["to"])
            ti.from_station = Station.objects.get(
                code=urllib.quote(de["from"].encode("utf-8")))
            ti.to_station = Station.objects.get(
                code=urllib.quote(de["to"].encode("utf-8")))
            ti.status = de.status
            ti.heading = de.dir if de.dir else -1
            ti.train_type = de.cat
            ti.timestamp = django.utils.timezone.now()
            ti.save()
        except KeyError:
            continue


def import_stations():
    moscow = Station()
    moscow.title = "Moskova"
    moscow.code = "MVA"
    moscow.latitude = "55.75"
    moscow.longitude = "37.6167"
    moscow.timestamp = django.utils.timezone.now()
    moscow.save()

    entries = {}
    for i in STATIONS:
        d = feedparser.parse(STATION_FEED_URL + i)
        if not d.has_key("bozo_exception"):
            (s, created) = Station.objects.get_or_create(title=d.feed.title, defaults={'code': i, 'latitude': 0, 'longitude': 0, 'timestamp': django.utils.timezone.now()})
            s.code = i
            try:
                geoco = d.feed[u'georss_point'].split()
                s.latitude = geoco[0]
                s.longitude = geoco[1]
            except KeyError:
                print "No coordinates for %s." % i
            s.timestamp = django.utils.timezone.now()
            s.save()
            entries[s] = d.entries
        else:
            logger.error(d["bozo_exception"])
    for s, e in entries.items():
        import_station_departures(s,e)


def import_station_departures(station, entries):
    for entry in entries:
        guid = entry.guid.split("/")[-1]
        print "%s (%s) %s -> %s" % (station.title, guid, urllib.quote(entry["fromstation"].encode("utf-8")), urllib.quote(entry["tostation"].encode("utf-8")))
        try:
            item = StationDepartures.objects.filter(station=station).get(guid=guid)
        except:
            item = StationDepartures()
            item.station = station
            item.guid = guid
        item.title = entry.title
        item.scheduledTime = entry.scheduledtime
        item.scheduledDepartTime = entry.scheduleddeparttime
        item.eta = entry.eta
        item.etd = entry.etd
        try:
            item.from_station = Station.objects.get(
                code=urllib.quote(entry["fromstation"].encode("utf-8")))
            item.to_station = Station.objects.get(
                code=urllib.quote(entry["tostation"].encode("utf-8")))
        except Station.DoesNotExist:
            print "STATION DOES NOT EXIST"
            continue
        item.completed = entry.completed
        item.status = entry.status
        item.lateness = entry.lateness
        item.timestamp = django.utils.timezone.now()
        item.save()



def import_arrivals(train):
    """Get arrivals and departures for a train (using GUID)"""
    d = feedparser.parse(TRAIN_DATA_URL + train)
    # if you can't find it, treat is programming error
    t = RunningTrain.objects.get(guid=train)
    if not d.has_key("bozo_exception"):
        tsi = RunningTrainStopInfo.objects.filter(train=t)
        for e in d.entries:
            si = Station.objects.get(code=e.stationcode)
            try:
                item = tsi.get(station=si)
            except:
                item = RunningTrainStopInfo()
                item.train = t
                item.station = si
                item.guid = e.guid.split("/")[-1]
            item.title = e.title
            item.scheduledTime = e.scheduledtime
            item.scheduledDepartTime = e.scheduleddeparttime
            item.eta = e.eta
            item.etd = e.etd
            item.completed = e.completed
            item.status = d.feed.status
            item.lateness = d.feed.lateness
            item.timestamp = django.utils.timezone.now()
            item.save()
    else:
        logger.error(d["bozo_exception"])
