import re

def validateIp(ip):
    pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'

    if not re.fullmatch(pattern, ip):
        return False

    splitted = ip.split('.')
    for chunk in splitted:
        if int(chunk) > 255:
            return False

    return True

def unpackHead(request):
    headBytes = request.split(b'\n')[0]
    head = headBytes.decode()

    splitted = head.split(' ')

    method = splitted[0]
    httpVersion = splitted[-1]
    uri = ' '.join(splitted[1:-1])

    return method, uri, httpVersion

def unpackUri(uri):
    if '?' not in uri:
        return uri, {}

    splitted = uri.split('?')
    route = splitted[0]

    strArgs = splitted[1]
    fragment = None

    args = {}

    for arg in strArgs.split('&'):
        key, value = arg.split('=')

        args[key] = value

    return route, args

def extractBody(request):
    index = 0
    bodyIndex = None

    while index < len(request):
        if request[index:index+4] == b'\r\n\r\n':
            bodyIndex = index + 4
            break

        elif request[index:index+2] == b'\n\n':
            bodyIndex = index + 2
            break

        index += 1

    if bodyIndex is None:
        return b''

    return request[bodyIndex:]