import json, base64
import urllib.request, urllib.error


class APIClient:
    def __init__(self, server_url, username, password):
        self.user = username
        self.password = password
        if not server_url.endswith('/'):
            server_url += '/'
            self.url = server_url + 'index.php?/api/v2/'

    def send_get(self, uri):
        return self.send_request('GET', uri, None)

    def send_post(self, uri, data):
        return self.send_request('POST', uri, data)

    def send_request(self, method, uri, data):
        url = self.url + uri
        request = urllib.request.Request(url)
        if method == 'POST':
            request.data = bytes(json.dumps(data), 'utf-8')
        auth = str(base64.b64encode(bytes('%s:%s' % (self.user, self.password), 'utf-8')), 'ascii').strip()
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')
        response = None
        response_error = None
        try:
            response = urllib.request.urlopen(request).read()
        except urllib.error.HTTPError as e:
            response_error = e.read()

        if response is not None:
            result = json.loads(response)
        else:
            result = {}

        if response_error is not None:
            if result and 'error' in result:
                raise APIError('TestRail API returned HTTP error' + str(response_error) + '"' + result['error'] + '"')

        return result


class APIError(Exception):
    pass


class FixClient:
    pass


class ItchClient:
    pass


class HurlClient:
    pass