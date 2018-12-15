import datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import *

# Create your views here.
# Note to self: do we need this view? People don't search for "what'll be on X frequency tomorrow night?"
class FreqList(ListView):
    template_name = 'shortwave/lookup.html'
    queryset = Station.objects.order_by('broadcaster')

    # Reference for this view:
    # URL format is /lookup/<freq>/<day>/<time>/
    # For now we are going for all days to simplify things but see below for info on adding a day_filter
    # **{day_filter: True} converts the day URL argument into a field name and returns stations with that day ticked
    def get_context_data(self, **kwargs):
        freq_filter = str(self.kwargs['freq'])
        #day_filter = str(self.kwargs['day'])
        time_filter = str(self.kwargs['time'])
        context = super(FreqList, self).get_context_data(**kwargs)
        context['station'] = Station.objects.filter(
        freq=freq_filter,
        timeon__lte=time_filter,
        timeoff__gte=time_filter,
        ).order_by('timeon', 'broadcaster')
        #context['widgets'] = TextItem.objects.order_by('sortorder')
        #context['pages'] = Page.objects.order_by('sortorder')
        return context

# This view takes the current time/day and filters on it for the /lookup/<freq>/now URL
class NowList(ListView):
    template_name = 'shortwave/lookup.html'
    queryset = Station.objects.order_by('broadcaster')

    # day_filter generates a lower-case day from the current datetime eg 'mon'
    # time_filter generates a string with the current time eg '13:45'
    def get_context_data(self, **kwargs):
        freq_filter = str(self.kwargs['freq'])
        day_filter = str(datetime.datetime.now().strftime('%a').lower())
        time_filter = str(datetime.datetime.now().strftime('%H:%M'))
        context = super(NowList, self).get_context_data(**kwargs)
        context['station'] = Station.objects.filter(
        freq=freq_filter,
        timeon__lte=time_filter,
        timeoff__gte=time_filter,
        **{day_filter: True}).order_by('timeon', 'broadcaster')
        #context['widgets'] = TextItem.objects.order_by('sortorder')
        #context['pages'] = Page.objects.order_by('sortorder')
        return context

# This view is for searching on broadcasters and languages etc
class ScheduleList(ListView):
    template_name = 'shortwave/schedule.html'
    queryset = Station.objects.order_by('broadcaster')

    # In this view we are checking whether /all/ is in the URL and if it is, we return a different set of filters
    # If /all/ is in the broadcaster slot then we only filter on language, and vice versa
    # URLconf for reference: path('schedule/<broadcaster>/<lang>/')
    def get_context_data(self, **kwargs):
        bc_filter = str(self.kwargs['broadcaster'])
        lang_filter = str(self.kwargs['lang'])
        context = super(ScheduleList, self).get_context_data(**kwargs)
        if bc_filter == 'all' and lang_filter == 'all':
            context['station'] = Station.objects.none() # return no stations to prevent clever users retrieving entire db with /all/all
        elif bc_filter == 'all':
            context['station'] = Station.objects.filter(lang__slug=lang_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        elif lang_filter == 'all':
            context['station'] = Station.objects.filter(broadcaster__slug=bc_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        else:
            context['station'] = Station.objects.filter(broadcaster__slug=bc_filter, lang__slug=lang_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        #context['widgets'] = TextItem.objects.order_by('sortorder')
        #context['pages'] = Page.objects.order_by('sortorder')
        return context

class ScheduleListWithTime(ListView):
    template_name = 'shortwave/schedule.html'
    queryset = Station.objects.order_by('broadcaster')

    # In this view we are checking whether /all/ is in the URL and if it is, we return a different set of filters
    # If /all/ is in the broadcaster slot then we only filter on language, and vice versa
    # URLconf for reference: path('schedule/<broadcaster>/<lang>/')
    def get_context_data(self, **kwargs):
        bc_filter = str(self.kwargs['broadcaster'])
        lang_filter = str(self.kwargs['lang'])
        time_filter = str(self.kwargs['time'])
        context = super(ScheduleListWithTime, self).get_context_data(**kwargs)
        if bc_filter == 'all' and lang_filter == 'all':
            # In this case we allow users to search on all/all/time because it is useful
            context['station'] = Station.objects.filter(timeon__lte=time_filter,
            timeoff__gte=time_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        elif bc_filter == 'all':
            context['station'] = Station.objects.filter(lang__slug=lang_filter, timeon__lte=time_filter,
            timeoff__gte=time_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        elif lang_filter == 'all':
            context['station'] = Station.objects.filter(broadcaster__slug=bc_filter,timeon__lte=time_filter,
            timeoff__gte=time_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        else:
            context['station'] = Station.objects.filter(broadcaster__slug=bc_filter, lang__slug=lang_filter,timeon__lte=time_filter,
            timeoff__gte=time_filter).order_by('freq', 'timeon', 'broadcaster', 'lang')
        #context['widgets'] = TextItem.objects.order_by('sortorder')
        #context['pages'] = Page.objects.order_by('sortorder')
        return context

# Simple view to return the details of an individual station by uuid
class StationDetail(DetailView):
    template_name = 'shortwave/station_detail.html'
    queryset = Station.objects.order_by('broadcaster')
    slug_field = 'uuid'

    def get_object(self):
        object = get_object_or_404(Station, uuid=self.kwargs['uuid'])
        return object

    def get_context_data(self, **kwargs):
        stn_filter = self.kwargs['uuid']
        context = super(DetailView, self).get_context_data(**kwargs)
        context['station'] = Station.objects.get(uuid=self.kwargs.get('uuid'))
        #context['widgets'] = TextItem.objects.order_by('sortorder')
        #context['pages'] = Page.objects.order_by('sortorder')
        return context

# Special view for the front page of the site
class FrontPage(ListView):
    template_name = 'shortwave/front.html'
    queryset = Station.objects.order_by('broadcaster')

    def get_context_data(self, **kwargs):
        context = super(FrontPage, self).get_context_data(**kwargs)
        context['station'] = Station.objects.all()
        context['broadcaster'] = Broadcaster.objects.all().order_by('broadcaster')
        context['language'] = Language.objects.all().order_by('language')
        context['solardata'] = SolarData.objects.all() # show only most recent solar data
        context['blogposts'] = BlogPost.objects.order_by("-datetime")[:5] # show 5x most recent blog posts
        context['pages'] = Page.objects.all().order_by('sortorder')
        return context

# Special view for content pages (eg. about)
class PageView(DetailView):
    template_name = 'shortwave/page.html'
    queryset = Page.objects.order_by('sortorder')

    def get_context_data(self, **kwargs):
        page_filter = self.kwargs['slug']
        context = super(PageView, self).get_context_data(**kwargs)
        context['pages'] = Page.objects.get(slug=self.kwargs.get('slug'))
        return context
