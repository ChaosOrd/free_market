from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'free_market_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'population.views.home_page', name='home'),
    url(r'^custom_population/$', 'population.views.custom_population',
        name='custom_population'),
)
