from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'free_market_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'population.views.home_page', name='home'),
    url(r'^population/', include('population.urls')),
    url(r'^accounts/', include('accounts.urls')),
)
