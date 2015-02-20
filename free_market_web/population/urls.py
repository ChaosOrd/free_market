from django.conf.urls import patterns, include, url
from django.contrib import admin
from population.views import ExistingUniverseView, NewUniverseView

urlpatterns = patterns('',
    url(r'^new_universe/$', NewUniverseView.as_view(), name='new_universe'),
    url(r'^universe/(\d+)/$', ExistingUniverseView.as_view(), name='universe')
)
