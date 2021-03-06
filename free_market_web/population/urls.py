from django.conf.urls import patterns, url
from population.views import (ExistingUniverseView, NewUniverseView,
                              my_universes_view, supply_demand_form,
                              delete_population, play_universe, simulation_result)

urlpatterns = patterns('',
    url(r'^new_universe/$', NewUniverseView.as_view(), name='new_universe'),
    url(r'^universe/(\d+)/$', ExistingUniverseView.as_view(), name='universe'),
    url(r'^universe/(\d+)/play/$', play_universe, name="play_universe"),
    url(r'^my_universes/$', my_universes_view, name='my_universes'),
    url(r'^delete_population/(\d+)/$', delete_population, name='delete_population'),
    url(r'^supply_demand_form/(\d+)$', supply_demand_form, name='supply_demand_form'),
    url(r'simulation_result/(\d+)/$', simulation_result, name='simulation_result')
)
