### Create An Application

[First, join Findings!](https://findings.com)

[create an application here](https://findings.com/me/applications)

Record your consumer key and secret. Be sure to set the callback url of your application.

### OAuth Client

Put your key and secret from your application into the API_SETTINGS in the client.

#### Example Application

See the "findingsdjango" directory in the github repository for an example Findings posting application.

### Terminology

Clip: A clip is a user's clip from a document. It contains information about when and who created it. It will contain the document, and the publisher of the document.

Document: A document is what a user's clip refers to. It's a piece of text with additionally an url (for a web document) or a set of book metadata (for a book clipping).

Page: Contains the next and previous urls for the next and previous set of data about this resultset.

### Caveats

Older documents do not have creation times.

### GET

Requires: a valid application key.

Base Url: https://findings.com/api/v1/

Returns: json

Methods:

* profile: https://findings.com/api/v1/(username)
* clips: https://findings.com/api/v1/(username)/clips
* clips for a particular document: https://findings.com/api/v1/clips/document/(document id)

Parameters:

* start_after: the element id for the next link the next pagination starts after
* start_before: the element id the link for previous pagination result starts before
* num: the number of items to return in the resultset

Examples:

Show this username's clips:

* https://findings.com/api/v1/jeffreyweston/clips?key=SOMEKEY

Show 10 of this username's clips using the previous link (and appending your key).

* https://findings.com/api/v1/jeffreyweston/clips?start_before=118060&num=10&key=SOMEKEY

### POST

Requires: a valid application key and an OAuth call with valid access tokens.

Base Url: /api/v1/

Returns: json

#### Post: Create A Clipping

* create new finding: https://findings.com/api/v1/(username)/clip

There are two kinds of clippings in Findings, book and web. To post a web clip you define the url, to post a book clip you must currently define the isbn (by title, author is coming soon).

Possible post parameters:

* isbn: if present the clipping is assigned to 'book'
* private: if not present, the private flag is set to false
* content: required. this is the clipping content
* url: if present, the clipping is assigned to 'web'
* note: a note about the clipping

So the required items are "content" and one of either "url" or "isbn".
