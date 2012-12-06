from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'labs.apps.apiclient.views.home', name='home'),
    url(r'^callback/$', 'labs.apps.apiclient.views.callback', name='callback'),
)
