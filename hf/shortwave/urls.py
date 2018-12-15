from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from . import views
from shortwave.views import *

urlpatterns = [
    path('',
    FrontPage.as_view()),

    path('schedule/<broadcaster>/<lang>/<time>',
    ScheduleListWithTime.as_view()),

    path('schedule/<broadcaster>/<lang>/',
    ScheduleList.as_view()),

    path('lookup/<int:freq>/now/',
    NowList.as_view()),

    #path('lookup/<int:freq>/<time>/',
    #FreqList.as_view()),

    path('detail/<uuid>/',
    StationDetail.as_view()),

    path('page/<slug>/',
    PageView.as_view()),

    url(r'^markdownx/', include('markdownx.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
