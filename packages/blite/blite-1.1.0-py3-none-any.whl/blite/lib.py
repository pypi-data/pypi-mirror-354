import socket as sk
from .utils import validateIp, unpackHead, unpackUri, extractBody
import re
from _thread import start_new_thread
import json
import sys
from .httpCodes import CODES
from .logger import Logger, LogLevel

def _stdInternalServerError():
    return b'HTTP/1.x 501 Internal Server Error\nConnection: close\n\n'

def _stdNotFoundError():
    return b'HTTP/1.x 404 Not Found\nConnection: close\n\n'

def _stdWrongMethod():
    return b'HTTP/1.x 405 Method Not Allowed\nConnection: close\n\n'

def renderFile(path):
    with open(path, 'r') as file:
        return file.read()

class Route:
    def __init__(self, route, callback, kwargs = (), methods = ['GET'], regex = False, allowOptions = True, giveMethod=False, giveUri=False, giveRequest=False):
        self.route = route
        self.callback = callback
        self.kwargs = kwargs
        self.methods = methods
        self.regex = regex
        self.allowOptions = allowOptions
        self.giveUri = giveUri
        self.giveMethod = giveMethod
        self.giveRequest = giveRequest

    def matches(self, uri, method):
        if self.regex:
            if not re.fullmatch(self.route, uri):
                return False

        else:
            if uri != self.route:
                return False

        if method in self.methods:
            return True

        if method.lower() == 'options':
            if self.allowOptions:
                return True

        return False

    def uriMatches(self, uri):
        if self.regex:
            if not re.fullmatch(self.route, uri):
                return False

        else:
            if uri != self.route:
                return False

        return True

class Response:
    def __init__(self, code, headers={'Connection: close'}, body=b''):
        if not isinstance(code, int):
            if not code.isnumeric():
                raise Exception('Wrong type for HTTP code')

        if not code in CODES:
            raise Exception('HTTP code not allowed')

        self.code = code

        if not isinstance(headers, dict):
            raise Exception('Headers must be expressed in dict')

        self.headers = headers
        self.body = body

    def representation(self):
        return f'HTTP/1.1 {self.cope} {CODES[self.code]} with body of type {type(self.body)}'

    def pack(self):
        return (f'HTTP/1.1 {self.code} {CODES[self.code]}' + '\n'.join(f'{key}: {value}' for key, value in self.headers.items()) + '\n\n').encode() + (self.body if isinstance(self.body, bytes) else self.body.encode())

class Server:
    def __init__(self, ip, port=80, standardHeaders={}, logLevel=LogLevel.CONCISE):
        if not validateIp(ip):
            raise Exception(f'Invalid IPv4 address: `{ip}`')

        if isinstance(port, int):
            if port < 0 or port > 65535:
                raise Exception(f'Port out of range 1-65535: `{port}`')

        else:
            raise Exception(f'Port must be an integer')

        self.__routes = []
        self.__standardHeaders = standardHeaders
        self.__logLevel = logLevel

        self.__sock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.__sock.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)

        self.__sock.bind((ip, port))

    def setStandardHeaders(self, headers):
        self.__standardHeaders = headers

    def setLogLevel(self, level):
        self.__logLevel = level

    def setRoute(self, route, kwargs=(), methods=['GET'], regex=False, allowOptions=True, giveMethod=False, giveUri=False, giveRequest=False):
        def decorator(callback):
            self.__routes.append(
                Route(
                    route=route, callback=callback, kwargs=kwargs, methods=methods, regex=regex,
                    allowOptions=allowOptions, giveMethod=giveMethod, giveUri=giveUri, giveRequest=giveRequest
                )
            )

        return decorator

    def __handler(self, client, address):
        try:
            requestBytes = client.recv(2048)

        except:
            client.send(_stdInternalServerError())
            client.close()
            return

        method, uri, _ = unpackHead(requestBytes)
        uri, kwargs = unpackUri(uri)

        if self.__logLevel == LogLevel.CONCISE:
            Logger.report(f'Incoming request: `{method} {uri}` from {address}')

        elif self.__logLevel == LogLevel.VERBOSE:
            Logger.report(f'Incoming request: `{method} {uri}` from {address}. Full request bytes: {requestBytes}')

        found = False
        rightRoute = None

        for route in self.__routes:
            if route.matches(uri, method):
                found = True
                rightRoute = route
                break

            if route.uriMatches(uri):
                found = True
                break

        if not found:
            if self.__logLevel:
                Logger.reportFailure(f'Failure handling incoming request: `{method} {uri}` from {address} because: 404 Uri Not Found')

            client.send(_stdNotFoundError())
            client.close()
            return

        if found and rightRoute is None:
            if self.__logLevel:
                Logger.reportFailure(f'Failure handling incoming request: `{method} {uri}` from {address} because: 405 Method Now Allowed')

            client.send(_stdWrongMethod())
            client.close()
            return

        if self.__logLevel:
            Logger.reportSuccess(f'Found route for `{method} {uri}` from {address}')

        if method == 'OPTIONS' and 'OPTIONS' not in rightRoute.methods:
            if self.__logLevel:
                Logger.reportSuccess(f'Answering with route options for `{method} {uri}` from {address}')
            client.send(
                f'HTTP/1.1 200 Ok\nConnection: close\n{"\n".join(f"{key}: {value}" for key, value in self.__standardHeaders)}\nAllow: {" ".join(rightRoute.methods)}\n\n'.encode()
            )
            client.close()
            return

        requestBody = extractBody(requestBytes)
        args = []

        if 'POST' in rightRoute.methods:
            args.append(requestBody)

        if rightRoute.giveMethod:
            args.append(method)

        if rightRoute.giveUri:
            args.append(uri)

        if rightRoute.giveRequest:
            args.append(requestBytes)

        try:
            responseBody = rightRoute.callback(*args, **kwargs)

        except TypeError:
            client.send(_stdInternalServerError())
            client.close()

            if self.__logLevel == LogLevel.CONCISE:
                Logger.reportFailure(f'Fatal failure handling `{method} {uri}` from {address}')

            elif self.__logLevel == LogLevel.VERBOSE:
                Logger.reportFailure(f'Fatal failure handling `{method} {uri}` from {address}')

            exceptionText = f'the callback function for "{method} {uri}" is expected to take at least {len(args)} positional argument(s): '
            expectedArgs = []

            if 'POST' in rightRoute.methods:
                expectedArgs.append('requestBody')

            if rightRoute.giveMethod:
                expectedArgs.append('method')

            if rightRoute.giveUri:
                expectedArgs.append('uri')

            if rightRoute.giveRequest:
                expectedArgs.append('requestBytes')

            raise Exception(exceptionText + ', '.join(expectedArgs))

        except Exception as e:
            if self.__logLevel == LogLevel.CONCISE:
                Logger.reportFailure(f'Fatal failure handling `{method} {uri}` from {address}')

            elif self.__logLevel == LogLevel.VERBOSE:
                Logger.reportFailure(f'Fatal failure handling `{method} {uri}` from {address}')

            print(f'Warning: callback function "{rightRoute.callback.__name__}" failed handling "{method} {uri}" because `{e}`', file=sys.stderr)
            client.send(_stdInternalServerError())
            client.close()
            return

        if responseBody is None:
            if self.__logLevel:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with empty OK response')

            client.send(f'HTTP/1.1 200 Ok\nConnection: close\n{"\n".join(f"{key}: {value}" for key, value in self.__standardHeaders)}\n\n'.encode())
            client.close()
            return

        responseHeaders = self.__standardHeaders

        if isinstance(responseBody, tuple):
            if not isinstance(responseBody[1], dict):
                client.send(_stdInternalServerError().encode())
                client.close()
                raise Exception('Response headers must be a dict')

            for key, value in responseBody[1].items():
                responseHeaders[key] = value

            responseBody = responseBody[0]

        for key, value in [('Connection', 'close'), ()]:
            if key not in responseHeaders:
                responseHeaders[key] = value

        if isinstance(responseBody, dict):
            strJson = json.dumps(responseBody)

            if 'Content-Type' not in responseHeaders:
                responseHeaders['Content-Type'] = 'application/json'

            if 'Content-Length' not in responseHeaders:
                responseHeaders['Content-Length'] = str(len(strJson))

            strHeaders= '\n'.join(f'{key}: {value}' for key, value in responseHeaders.items())

            if self.__logLevel:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with OK response containing {responseHeaders["Content-Type"]}')

            client.send(
                f'HTTP/1.1 200 Ok\n{strHeaders}\n\n{strJson}'.encode()
            )
            client.close()
            return

        elif isinstance(responseBody, str):
            if 'Content-Type' not in responseHeaders:
                responseHeaders['Content-Type'] = 'text/plain'

            if 'Content-Length' not in responseHeaders:
                responseHeaders['Content-Length'] = str(len(responseBody))

            strHeaders = '\n'.join(f'{key}: {value}' for key, value in responseHeaders.items())

            if self.__logLevel:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with OK response containing {responseHeaders["Content-Type"]}')

            client.send(
                f'HTTP/1.1 200 Ok\n{strHeaders}\n\n{responseBody}'.encode()
            )
            client.close()
            return

        elif isinstance(responseBody, bytes):
            if 'Content-Type' not in responseHeaders:
                responseHeaders['Content-Type'] = 'application/bytes'

            if 'Content-Length' not in responseHeaders:
                responseHeaders['Content-Length'] = str(len(responseBody))

            strHeaders = '\n'.join(f'{key}: {value}' for key, value in responseHeaders.items())

            if self.__logLevel:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with OK response containing {responseHeaders["Content-Type"]}')

            client.send(
                f'HTTP/1.1 200 Ok\n{strHeaders}\n\n'.encode() + responseBody
            )
            client.close()
            return

        elif isinstance(responseBody, Response):
            if self.__logLevel == LogLevel.CONCISE:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with OK custom response')

            elif self.__logLevel == LogLevel.VERBOSE:
                Logger.reportSuccess(f'Answering to `{method} {uri}` from {address} with OK custom response: {Response.representation()}')

            client.send(responseBody.pack())
            client.close()
            return

        else:
            if self.__logLevel:
                Logger.reportFailure(f'Fatal failure handling `{method} {uri}` from {address} because of internal server error')

            client.send(_stdInternalServerError().encode())
            client.close()
            raise Exception(f'Unexpected return type: `{type(responseBody)}`')

    def listen(self):
        self.__sock.listen()

        while True:
            client, address = self.__sock.accept()
            start_new_thread(self.__handler, (client, address))