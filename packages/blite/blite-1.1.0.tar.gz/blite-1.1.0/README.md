# blite
- minimal web backend framework

# Usage
- first step is to import the library and instantiate a `Server` object, passing the host and port to bind to the server

```python
from blite import Server, renderFile

HOST = '0.0.0.0'
PORT = 8080

server = Server(HOST, PORT)
```
- logging level can be set to:
  - silent executing `server.setLogLevel(LogLevel.SILENT)`
  - concise executing `server.setLogLevel(LogLevel.CONCISE)`
  - verbose executing `server.setLogLevel(LogLevel.VERBOSE)`

- then define the routes, using the `@server.setRoute()` decorator
    - the decorator requires a route parameter, which is the URI relative to the callback function

```python
@server.setRoute('/')
def root():
    return renderFile('index.html')
```

- additional parameters can be given to the decorator, such as
    - `methods: [str]` which defaults to `['GET']`
        - methods must be specified to be accepted by the framework, otherwise it will answer to the client with a `405 Method Now Allowed` HTTP response
    - `regex: bool` which defaults to `False`
        - indicates that the route is specified as a regex pattern
    - `allowOptions: bool` which defaults to `True`
        - tells the framework if it should answer to `OPTIONS` requests for the given route
    - `giveMethod: bool` which defaults to `False`
        - if set to True, the framework will provide the callback function with the method used by the client
    - `giveUri: bool` which defaults to `False`
        - if set to True, the framework will provide the callback function with the uri called by the client
    - `giveRequest: bool` which defaults to `False`
        - if set to True, the framework will provide the callback with the request bytes
    - `kwargs: tuple(str)` which defaults to `()`
        - if the tuple is populated, the framework will expect parameters to be given into the URI
        - e.g. `http://HOST:PORT/URI?key=value&other_key=other_value`

- callback functions can either return someting or `None`
- allowed return values (different from `None`) are
    - `string`, which is intended as response body
    - `bytes`, which is indended as response body
    - `tuple(headers: dict, responseBody: Any)`
    - `dict`, which is intended as json response body
    - `Response`
        - custom class which allows to set HTTP code, response headers and response body

- for full usage example, take a look at the following code

# Usage Example

```python 
from blite import Server, Response, renderFile, HttpCode, LogLevel
import json

HOST = '0.0.0.0'
PORT = 8080

server = Server(HOST, PORT)

# set the headers to be used in every HTTP response   
server.setStandardHeaders({'Access-Control-Allow-Origin' : '*'})

# sets concise logging level
server.setLogLevel(LogLevel.CONCISE)

@server.setRoute('/')
def root():
    renderFile('index.html')


@server.setRoute('/auth', kwargs=('wants_token'), methods=['POST'], allowOptions=False)
def authUser(requestBody, wants_token):
    try:
        jData = json.loads(requestBody.decode())

    except:
        return Response(code=HttpCode.NOT_FOUND)

    uname = jData.get('username')
    passwd = jData.get('password')

    if uname is None or passwd is None:
        return Response(code=HttpCode.NOT_FOUND)

    authenticated = checkCredentials(uname, passwd)  # function defined elsewhere

    if not authenticated:
        return 'failed'

    if wants_token == 'true':
        token = makeToken(uname, passwd)  # function defined elsewhere
        return {'token': token}

    return 'ok'


@server.setRoute('/get_data', methods=['POST'], giveMethod=True)
def getData(requestBody, method):
    try:
        jData = json.loads(requestBody.decode())
    except:
        return Response(code=HttpCode.NOT_FOUND)

    authenticated = checkAuthentication(jData)  # function defined elsewhere
    if not authenticated:
        return Response(code=HttpCode.FORBIDDEN)

    jsonData = fetchData()  # function defined elsewhere, which returns a dict
    return jsonData


@server.setRoute('^/get_image/[0-9a-zA-Z]*\.(jpg|png|jpeg)\/?$', regex=True, giveUri=True)
def getImage(uri):
    imagePath = findImagePath(uri)  # function defined elsewhere
    imageBytes = getImageBytes(imagePath)  # function defined elsewhere

    if not imageBytes:
        return Response(code=HttpCode.NOT_FOUND)

    imageExtension = imagePath.split('.')[-1]
    return {'Content-Type': f'image/{imageExtension}'}, imageBytes
```