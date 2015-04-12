from django.conf.urls import patterns, include, url

urlpatterns = [
        url('^', include('django.contrib.auth.urls'))
]
