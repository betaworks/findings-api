### Create An Application

[First, join Findings!](https://findings.com)
[create an application here](https://findings.com/me/applications)
Record your consumer key and secret. Be sure to set the callback url of your application.

### OAuth Client

Put your key and secret from your application into the API_SETTINGS in the client.

#### Example Application

See the "django-findings" directory for an example findings posting application.

### GET

Requires: a valid application key.
Base Url: https://findings.com/api/v1/
Methods:

* profile: (username)
* clips: (username)/clips
* clips for a particular document: clips/document/(document id)

### POST

Requires: a valid application key and an OAuth call with valid access tokens.
Base Url: /api/v1/
Methods:

* create new finding: username/clip
