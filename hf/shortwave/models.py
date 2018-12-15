import uuid
from django.db import models
from markdownx.models import MarkdownxField

# Create your models here.
class LanguageManager(models.Manager):
    def get_by_natural_key(self, slug_):
        return self.get(slug=slug_)

class Language(models.Model):
    language = models.CharField(max_length=128)
    slug = models.CharField(max_length=64)

    objects = LanguageManager()

    def natural_key(self):
        return(self.slug,)

    def publish(self):
        self.save()

    def __str__(self):
        return self.language

class BroadcasterManager(models.Manager):
    def get_by_natural_key(self, slug_):
        return self.get(slug=slug_)

class Broadcaster(models.Model):
    broadcaster = models.CharField(max_length=128)
    url = models.URLField(blank=True, null=True)
    slug = models.CharField(max_length=64)

    objects = BroadcasterManager()

    def natural_key(self):
        return(self.slug,)

    def publish(self):
        self.save()

    def __str__(self):
        return self.broadcaster

class SiteManager(models.Manager):
    def get_by_natural_key(self, slug_):
        return self.get(slug=slug_)

class Site(models.Model):
    site = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=8, decimal_places=4)
    lon = models.DecimalField(max_digits=8, decimal_places=4)
    iso = models.CharField(max_length=3)
    countryslug = models.CharField(max_length=3)
    countryname = models.CharField(max_length=128)

    objects = SiteManager()

    def natural_key(self):
        return(self.slug,)

    def publish(self):
        self.save()

    def __str__(self):
        return self.site

class Station(models.Model):
    freq = models.IntegerField()
    timeon = models.TimeField()
    timeoff = models.TimeField()
    mon = models.BooleanField(blank=True)
    tue = models.BooleanField(blank=True)
    wed = models.BooleanField(blank=True)
    thu = models.BooleanField(blank=True)
    fri = models.BooleanField(blank=True)
    sat = models.BooleanField(blank=True)
    sun = models.BooleanField(blank=True)
    broadcaster = models.ForeignKey('Broadcaster', on_delete=models.DO_NOTHING)
    site = models.ForeignKey('Site', on_delete=models.DO_NOTHING, null=True, blank=True)
    lang = models.ForeignKey('Language', on_delete=models.DO_NOTHING, null=True, blank=True)
    power = models.IntegerField()
    azimuth = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    uuid = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
            super().save(*args, **kwargs)

    def __str__(self):
        return str(self.freq)

class Page(models.Model):
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    content = MarkdownxField()
    sortorder = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.title)

class SolarData(models.Model):
    datetime = models.DateTimeField(auto_now=True) # to show last time of update
    solarflux = models.IntegerField()
    aindex = models.IntegerField()
    kindex = models.IntegerField()
    sunspots = models.IntegerField()
    geomagfield = models.CharField(max_length=16)
    signalnoise = models.CharField(max_length=16)

    def publish(self):
        self.save()

    def __str__(self):
        return str("Solar data: " + str(self.datetime))

class BlogPost(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=256)
    link = models.URLField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.title)
