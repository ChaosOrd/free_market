from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

sign_up_done_view = TemplateView.as_view(template_name='sign_up_done.html')

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^sign_up/', CreateView.as_view(
        template_name='sign_up.html',
        form_class=UserCreationForm,
        success_url='../sign_up_done/'
    ), name='sign_up'),
    url(r'^sign_up_done/', sign_up_done_view, name='sign_up_done'),
]
