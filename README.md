### Create An Application

[First, join Findings!](https://findings.com)

[create an application here](https://findings.com/me/applications)

Record your consumer key and secret. Be sure to set the callback url of your application.

### OAuth Client

Put your key and secret from your application into the API_SETTINGS in the client.

#### Example Application

See the "findingsdjango" directory for an example findings posting application.

### Terminology

Clip: A clip is a user's clip from a document. It contains information about when and who created it. It will contain the document, and the publisher of the document.

Document: A document is what a user's clip refers to. It's a piece of text with additionally an url (for a web document) or a set of book metadata (for a book clipping).

Page: Contains the next and previous urls for the next and previous set of data about this resultset.

### Caveats

Older documents do not have creation times.

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
