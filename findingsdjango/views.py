from django.http import HttpResponse, Http404
from django.template import Context, Template, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.conf import settings

from labs.apps.apiclient.models import AccessToken
from labs.apps.apiclient.client import FindingsAPIClient


API_KEY = 'somekey'
API_SECRET = 'somesecret'


def callback(request):
    # callback happens from the redirect_uri you've provided
    # we're handed the code and state from BACK from the api server
    state = request.GET.get("state")
    code = request.GET.get("code")
    # build the client
    client = FindingsAPIClient(API_KEY, API_SECRET)
    # ask the provider for the final access_token
    response = client.get_access_token(code, state)
    if response.get("access_token"):
        # save the token locally
        access_token, created = AccessToken.objects.get_or_create(
            access_token=response.get("access_token"),
            expires_in=response.get("expires_in"),
            refresh_token=response.get("refresh_token"),
            )
        # we're done, go home
        return redirect("/apiclient/")
    return HttpResponse()


def home(request):
    # build the client
    client = FindingsAPIClient(API_KEY, API_SECRET)
    clips = client.fetch_clips()
    # is there an existing saved token?
    try:
        access_token = AccessToken.objects.all()[0]
    except IndexError:
        access_token = None
    return render_to_response(
        "api.html", {
        "clips": clips,
        "auth_url": client.auth_url(),
        "access_token": access_token,
        },
        context_instance=RequestContext(request)
        )
