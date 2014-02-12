from django.db import models
from django import forms
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
    title = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, db_index=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return "(%s)%s (%f,%f)" % (self.code, self.title, self.latitude, self.longitude)


class StationDepartures(models.Model):

    """Scheduled Train stopping at the Station, 
    not necessarily a running train"""
    station = models.ForeignKey(Station)
    guid = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    scheduledTime = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    scheduledDepartTime = forms.TimeField(widget=forms.TimeInput(
        format='%H:%M'))
    from_station = models.ForeignKey(Station, related_name="+")
    to_station = models.ForeignKey(Station, related_name="+")
    eta = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    etd = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    status = models.CharField(max_length=2, choices=TRAIN_STATUS)
    lateness = models.IntegerField()
    category = models.CharField(max_length=1)
    completed = models.BooleanField()
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = ('station', 'guid')

    def __unicode__(self):
        return "(%s)%s (%s,%s)" % (self.station.title, self.guid, self.from_station, self.to_station)


class RunningTrain(models.Model):

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


class RunningTrainStopInfo(models.Model):

    """Station data for a train"""
    train = models.ForeignKey(RunningTrain)
    guid = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    scheduledTime = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    scheduledDepartTime = forms.TimeField(widget=forms.TimeInput(
        format='%H:%M'))
    eta = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    etd = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
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
