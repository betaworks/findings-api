from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'login/', 'labs.findingsapi.views.login'),
    url(r'callback/', 'labs.findingsapi.views.callback'),
    url(r'clear/', 'labs.findingsapi.views.clear'),
    url(r'sendclip/', 'labs.findingsapi.views.sendclip'),
    url(r'', 'labs.findingsapi.views.home'),
)
