import urlparse
import urllib
from urllib2 import urlopen, URLError, HTTPError
import simplejson
from simplejson import JSONDecodeError

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, Template, loader, RequestContext
from django.template.loader import select_template, render_to_string
from django.shortcuts import render_to_response, get_object_or_404

from labs.findings_client import FindingsOAuthClient, API_SETTINGS, API_URL
from labs.findingsapi.models import FindingsArticleForm

def _single(request, data):
    templates = ["base.html"]
    if data.has_key("template"):
        templates = [data['template']]
    tpl = select_template(templates)
    return render_to_response(tpl.name,
        {'data':data},
        context_instance=RequestContext(request)
        )

def home(request):
    data = {}
    data['msg'] = None
    form = False
    if request.session.has_key("oauth"):
        data['oauth'] = request.session['oauth']
        form = FindingsArticleForm
        urls = {
            'profile':'%s/%s?key=%s' % (
                API_URL,
                data['oauth']['screen_name'],
                API_SETTINGS['key']),
            'clipdata':'%s/%s/clips?num=3&key=%s' % (
                API_URL,
                data['oauth']['screen_name'],
                API_SETTINGS['key']),
            }
        for k,v in urls.iteritems():
            try:
                result = urlopen(v).read()
                data[k] = simplejson.loads(result)
            except (URLError, HTTPError):
                result = None
        data['clips'] = data['clipdata'][0]['clips']
    else:
        data['oauth'] = False
        data['clips'] = None
    if request.POST:
        form = FindingsArticleForm(request.POST)
        if form.is_valid():
            # being the api post process
            posted = post_finding(request, form)
            if posted.has_key("error"):
                data['msg'] = posted['error']
            else:
                return HttpResponseRedirect('/findingsapi/')
    data['form'] = form
    return _single(request, data)

def post_finding(request, form):
    # first save the information locally
    article = form.save()
    # now construct the api call using the
    # session access_token
    post_params = {
        'oauth_token': request.session['oauth']['oauth_token'],
        'oauth_token_secret': request.session['oauth']['oauth_token_secret'],
        'user_id': request.session['oauth']['user_id'],
        'content': article.clipping,
        'url': article.url,
        'isbn': article.isbn,
        }
    client = FindingsOAuthClient()
    return client.post_clip(post_params)

def login(request):
    client = FindingsOAuthClient()
    url = client.login()
    # session or some other storage mechanism
    request.session['request_token'] = dict(urlparse.parse_qsl(url))
    return HttpResponseRedirect(url)

def clear(request):
    del(request.session['oauth'])
    return HttpResponseRedirect("/findingsapi/")

def callback(request):
    """
    the return from the oauth provider should look like:
    {'oauth_token_secret': '16WvEbqFWg6m', 'user_id': '136', 'oauth_token': 'EPBO4XsoSezc', 'screen_name': 'jeffreyweston'}

    it is now the client's responsibility to set the local session with the appropirate user and
    to store the oauth information
    """
    client = FindingsOAuthClient()
    oauth_token = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']
    oauth_token_secret = request.session['request_token']['oauth_token_secret']
    access_information = client.callback(oauth_token,
                       oauth_token_secret,
                       oauth_verifier)
    # some storage mechanism, just session here for testing
    request.session['oauth'] = access_information
    return _single(request, {
        'close_window': True,
        'template': 'callback.html',
        })
