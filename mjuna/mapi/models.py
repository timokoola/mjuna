from django.db import models

# Create your models here.


TRAIN_STATUS = (
    ('1', 'in time'),
    ('2', 'late'),
    ('4', 'very late'),
    ('5', 'cancelled')
)

TRAIN_TYPE = (
    ('S', 'Pendolino'),
    ('IC', ' InterCity'),
    ('IC2', 'InterCity2'),
    ('P', 'Express,'),
    ('H', 'Henkilojuna'),
    ('AE', ' Allegro')
)


class Station(models.Model):
    """Presentation of railway station"""
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10, db_index=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return "(%s)%s (%f,%f)" % (self.code, self.title, self.latitude, self.longitude)


class TrainInfo(models.Model):
    """Train moving on a map"""
    guid = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=1)
    title = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    from_station = models.ForeignKey(Station, related_name="+")
    to_station = models.ForeignKey(Station, related_name="+")
    status = models.CharField(max_length=2, choices=TRAIN_STATUS)
    heading = models.IntegerField()
    train_type = models.CharField(max_length=3, choices=TRAIN_TYPE)
    reason_code = models.TextField()
    timestamp = models.DateTimeField()


    def __unicode__(self):
        return "(%s)%s (%s -> %s)" % (self.guid, self.title, self.from_station, self.to_station)


class TrainStationInfo(models.Model):

    """Station data for a train"""
    train = models.ForeignKey(TrainInfo)
    guid = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    scheduledTime = models.DateTimeField()
    scheduledDepartTime = models.DateTimeField()
    eta = models.DateTimeField()
    etd = models.DateTimeField()
    station = models.ForeignKey(Station)
    completed = models.BooleanField()
    status = models.CharField(max_length=2, choices=TRAIN_STATUS)
    lateness = models.IntegerField()
    timestamp = models.DateTimeField()

    def completed_str(self):
        if self.completed:
            return "Arrived"
        else:
            return "Not yet"

    def __unicode__(self):
        return "%s (%s) Arriving: %s, Leaving: %s. Status: %s" % (self.train, self.completed_str, self.eta.isoformat(), self.etd.isoformat(), self.status)
