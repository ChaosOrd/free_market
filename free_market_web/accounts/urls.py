from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

sign_up_done_view = TemplateView.as_view(template_name='sign_up_done.html')

urlpatterns = [
    url(r'^sign_up/$', CreateView.as_view(
        template_name='sign_up.html',
        form_class=UserCreationForm,
        success_url='../sign_up_done/'
    ), name='sign_up'),
    url(r'^sign_up_done/$', sign_up_done_view, name='sign_up_done'),
    url(r'^log_in/$', login, {'template_name': 'log_in.html'}, name='log_in'),
    url(r'^log_out/&', logout, {'template_name': 'home.html'},
        name='log_out')
]
