from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'login/', 'labs.findingsdjango.views.login'),
    url(r'callback/', 'labs.findingsdjango.views.callback'),
    url(r'clear/', 'labs.findingsdjango.views.clear'),
    url(r'sendclip/', 'labs.findingsdjango.views.sendclip'),
    url(r'', 'labs.findingsdjango.views.home'),
)
