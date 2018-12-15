from django.contrib import admin
#from .models import Language, Broadcaster, Station, Site
from .models import *

# Register your models here.
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'slug')
    ordering = ('language',)
admin.site.register (Language, LanguageAdmin)

class BroadcasterAdmin(admin.ModelAdmin):
    list_display = ('broadcaster', 'url', 'slug')
    ordering = ('broadcaster',)
admin.site.register (Broadcaster, BroadcasterAdmin)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'site', 'slug', 'lat', 'lon', 'iso', 'countryname')
    ordering = ('site',)
admin.site.register (Site, SiteAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ('freq', 'broadcaster', 'timeon', 'timeoff', 'lang', 'site', 'power', 'azimuth', 'uuid')
    ordering = ('freq', 'broadcaster')
admin.site.register (Station, StationAdmin)

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'sortorder')
    ordering = ('sortorder',)
admin.site.register (Page, PageAdmin)

class SolarDataAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'solarflux', 'aindex', 'kindex', 'sunspots', 'geomagfield', 'signalnoise')
    ordering = ('datetime',)
admin.site.register (SolarData, SolarDataAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'datetime')
admin.site.register(BlogPost, BlogPostAdmin)
