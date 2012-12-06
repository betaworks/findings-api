## GET A KEY/SECRET

https://findings.com/user/applications

## TURN YOUR KEY SIR

https://findings.com/api/v1/clip/?format=json&key=YOUR-DARN-KEY

You'll see source urls in there. Follow them. Note the META at the top of these datasets. They should have everything you need to tunnel down, paginate, etc.

## TAKE NOTE BUCKEY

Note: GET requests require an api key

Note: POST requests require an access_token

Note: There is only 1 POST request allowed, which is to post a clip via

https://findings.com/api/v1/clip/

## ACCESS TOKEN

See the findingsdjango/views file for an example in getting an access token. It is oauth2. Not python-oauth2, which is actually oauth 1.0a. When the world decides oauth and python oauth doesn't need to be a clusterfuck anymore, I won't feel the need to point it out anymore.