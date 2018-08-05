import json, base64
import urllib.error
import urllib.parse
import urllib.request
from json import JSONDecodeError
from test_definitions import BaseConfig


class HTTPClient:
    def __init__(self, server_url):
        self.user = BaseConfig.TESTRAIL_USER
        self.password = BaseConfig.TESTRAIL_PASSWORD
        self.testrail_uri = 'index.php?/api/v2/'
        self.guerrilla_uri = 'ajax.php?f='
        if not server_url.endswith('/'):
            server_url += '/'
            if 'guerrilla' in server_url:
                self.authorization = False
                self.url = server_url + self.guerrilla_uri
            elif 'testrail' in server_url:
                self.authorization = True
                self.url = server_url + self.testrail_uri

    def send_get(self, uri, _token=None):
        return self.send_request('GET', uri, None, _token)

    def send_post(self, uri, data, _token=None):
        return self.send_request('POST', uri, data, _token)

    def send_request(self, method, uri, data=None, _token=None):
        result = None
        response = None
        response_error = None
        url = self.url + uri
        request = urllib.request.Request(url)
        if self.authorization is True:
            auth = str(base64.b64encode(bytes('%s:%s' % (self.user, self.password), 'utf-8')), 'ascii').strip()
            request.add_header('Authorization', 'Basic %s' % auth)
            request.add_header('Content-Type', 'application/json')
            if method == 'POST':
                request.data = bytes(json.dumps(data), 'utf-8')
            try:
                response = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                response_error = e.read()
            if response:
                status = response.status
                body = json.loads(response.read())
                result = [status, body, ]
            if response_error:
                if result and 'error' in result:
                    raise APIError(
                        'TestRail API returned HTTP error' + str(response_error) + '"' + response.read()['error'] + '"')
            return result
        elif self.authorization is False:
            if method == 'POST':
                data = urllib.parse.urlencode(data)
                url_encoded = url + "{0}".format(data)
                request.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/67.0.3396.99 Safari/537.36')
                request.add_header('Cookie', 'PHPSESSID=' + _token)
                try:
                    response = urllib.request.urlopen(url_encoded)
                except urllib.error.HTTPError as e:
                    response_error = e.read()
            elif method == 'GET':
                request.add_header('Content-Type', 'application/json')
                request.add_header('User-Agent',
                                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                   'Chrome/67.0.3396.99 Safari/537.36')
                if _token:
                    request.add_header('Cookie', 'PHPSESSID=' + _token)
                try:
                    response = urllib.request.urlopen(request)
                except urllib.error.HTTPError as e:
                    response_error = e.read()
            if response:
                status = response.status
                cookie = response.getheader('Set-Cookie')
                try:
                    body = json.loads(response.read())
                except JSONDecodeError:
                    body = response.read().decode('utf-8')
                result = [status, body, cookie]
            if response_error:
                if result and 'error' in result:
                    raise APIError(
                        'Guerrilla API return HTTP error' + str(response_error) + '"' + response.read()['error'] + '"')
            return result


class APIError(Exception):
    pass
