import time
import simplejson
import oauth2 as oauth
import urlparse, urllib, urllib2
from urllib2 import URLError, HTTPError

API_URL = 'https://findings.com/api/v1'
API_OAUTH_URL = 'https://findings.com/oauth'
API_SETTINGS = {
    'key':'some-key',
    'secret':'some-secret',
    'url':{
      'profile':'%s/me' % (API_URL),
      'get_clips':'%s/me/clips' % (API_URL),
      'post_clip':'%s/clip/new' % (API_URL),
      'request_token':'%s/request_token' % (API_OAUTH_URL),
      'authenticate':'%s/authenticate' % (API_OAUTH_URL),
      'access_token':'%s/access_token' % (API_OAUTH_URL),
      }
    }

class FindingsOAuthClient:

    def __init__(self):
        self.consumer = oauth.Consumer(
            key=API_SETTINGS['key'],
            secret=API_SETTINGS['secret'])

    def build_request(self, url, key, secret, method):
        params = {
            'oauth_version': "1.0",
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
            'oauth_signature_method': 'HMAC-SHA1',
            }
        params['oauth_consumer_key'] = self.consumer.key
        req = oauth.Request(method=method, url=url, parameters=params)
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        req.sign_request(signature_method, self.consumer, None)
        return req

    def request_token(self, url, key, secret, method='GET'):
        request = self.build_request(url, key, secret, method)
        query_string = urllib.urlencode(request)
        if method == 'GET':
            url = "%s?%s" % (url, query_string)
            response = urllib2.urlopen(url)
        else:
            u = urllib2.Request(url, query_string)
            response = urllib2.urlopen(u)
        return response.read()

    def login(self):
        """
        call the oauth server and ask for a request token via "request_token"

        then use the request token to setup a call to the authentication page
        on the oauth server

        once the user has authenticated and allowed the application,
        they will be sent to the callback url with the token and verifier
        """
        response = self.request_token(
            API_SETTINGS['url']['request_token'],
            API_SETTINGS['key'],
            API_SETTINGS['secret']
            )
        url = "%s?%s" % (API_SETTINGS['url']['authenticate'], response)
        return url

    def callback(self, oauth_token, oauth_token_secret, oauth_verifier):
        """
        the callback url is part of the oauth application
        setting on server side and doesn't need to be set in your code

        this is the callback landing from the oauth server
        at this point the session's request_token['oauth_token']
        must match the returned request token, and use the session's
        oauth_token_secret and returned verifier to construct
        request for the access token

        the returned content body from access_token should include:
        oauth_token_secret, user_id, oauth_token, screen_name
        """
        token = oauth.Token(oauth_token, oauth_token_secret)
        token.set_verifier(oauth_verifier)
        client = oauth.Client(self.consumer, token)
        resp, content = client.request(
            API_SETTINGS['url']['access_token'],
            "POST"
            )
        userinfo_and_tokens = dict(urlparse.parse_qsl(content))
        return userinfo_and_tokens

    def post_clip(self, clip_data):
        """
        clip data is a dict
        but there may be a status return as well
        return a tuble with success, and data or a message
        """
        url = API_SETTINGS['url']['post_clip']
        data = urllib.urlencode(clip_data)
        request = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(request)
        except HTTPError, e:
            # in proper data formating will result in a 400
            return False
        # the json returned will be either the clip, or an error message
        return simplejson.loads(response.read())
