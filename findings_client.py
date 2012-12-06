import time
import hashlib
import random
import urllib
import urllib2
import simplejson


class FindingsAPIClient:

    URLS = {
        "auth_url": "https://findings.com/oauth2/authorize/?client_id=%s&scope=%s&state=%s&response_type=%s&redirect_uri=%s",
        "token": "https://findings.com/oauth2/token/",
        "callback_url": "http://YOURSITE/apiclient/callback/",
        "create_clip": "https://findings.com/api/v1/clip/?access_token=%s",
        "clips": "https://findings.com/api/v1/clip/?format=json&key=%s"
        }

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.callback = self.URLS["callback_url"]

    def gen_nonce(self):
        h = hashlib.md5()
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        h.update(str(time.time()) + str(random_number))
        return h.hexdigest()

    def auth_url(self, scope=""):
        # generate the auth-url for the initial code request
        return self.URLS["auth_url"] % (
            self.key,
            scope,
            self.gen_nonce(),
            "code",
            self.callback
            )

    def get_access_token(self, code, state):
        # given a code and a state from the api server
        # ask the api server for an access_token
        url = self.URLS["token"]
        values = {
            "client_id": self.key,
            "client_secret": self.secret,
            "code": code,
            "state": state,
            "grant_type": "authorization_code",
            "response_type": "token",
            "redirect_uri": self.callback,
            }
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        result = response.read()
        # eg {'access_token': '82d2d10e55', 'token_type': 'bearer',
        # 'expires_in': 31536000, 'refresh_token': 'd70f32b995', 'scope': ''}
        return simplejson.loads(result)

    def fetch_clips(self):
        url = self.URLS["clips"] % (self.key)
        f = urllib2.urlopen(url)
        data = simplejson.loads(f.read())
        clips = [n for n in data.get("objects", [])]
        return clips
