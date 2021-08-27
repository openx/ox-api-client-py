from collections import namedtuple
import logging
import requests
from requests_oauthlib import OAuth1Session

log = logging.getLogger('oauth1_session')
# log.setLevel('DEBUG')

AuthData = namedtuple('AuthData', 'customer_key customer_secret realm')


class OXApiClient:
    pass


def wrap_rest_method(old_method):
    def new_method(self: OXApiClient, url: str, *args, **kwargs):
        req_url = self._prefix_url(url)
        self._add_cookie_to_kwargs(kwargs)
        self._add_client_to_kwargs(kwargs)
        return old_method(self, req_url, *args, **kwargs)

    new_method.__doc__ = old_method.__doc__
    new_method.__name__ = old_method.__name__
    return new_method



class OXApiClient:
    def __init__(self, customer_key=None, customer_secret=None, domain=None, realm=None, api_hostname=None):
        self.base_authorization_url = 'https://' + domain if domain else 'https://sso.openx.com'
        self._auth_data = AuthData(customer_key, customer_secret, realm)
        self._oauth_session = None
        self._request_token = None
        self.access_token = None
        self.api_hostname = api_hostname

    def obtain_request_token(self, callback_uri='oob'):
        self._oauth_session = OAuth1Session(self._auth_data.customer_key, self._auth_data.customer_secret,
                                            callback_uri=callback_uri)
        self._request_token = self._oauth_session.fetch_request_token(
            self.base_authorization_url + '/api/index/initiate',
            self._auth_data.realm)

    def login(self, username=None, password=None):
        if username and password:
            self.obtain_request_token()
            url = self._oauth_session.authorization_url(self.base_authorization_url + '/login/process',
                                                        self._request_token['oauth_token'])
            authorization = self._oauth_session.post(url, data={
                'email': username,
                'password': password,
                'oauth_token': self._request_token['oauth_token']
            })
            redirect_url = authorization.content.decode()
            response = self._oauth_session.parse_authorization_response(redirect_url)
            self.access_token = self._oauth_session.fetch_access_token(self.base_authorization_url + '/api/index/token',
                                                                       response['oauth_verifier'])
        else:
            from ox_api_cli.client.browser_login import BrowserLogin
            blogin = BrowserLogin(self)
            blogin.interactive_login()
        self._oauth_session.headers.update({'content-type': 'application/json', 'accept': 'application/json'})

    def _add_cookie_to_kwargs(self, kwargs):
        """
        Ensures the request will have a 'cookies' arg with 'openx3_access_token' cookie
        :param kwargs:
        :return:
        """
        cookies = kwargs.get('cookies', {})
        cookies.update({'openx3_access_token': self.access_token['oauth_token']})
        kwargs.update({'cookies': cookies})
        return kwargs

    def _add_client_to_kwargs(self, kwargs):
        """
        Ensures the request will have a 'headers' arg with 'X-OpenX-Client' header
        :param kwargs:
        :return:
        """
        headers = kwargs.get('headers', {})
        headers.update({'X-OpenX-Client': 'ox_api_cli v0.1'})
        kwargs.update({'headers': headers})
        return kwargs

    def _prefix_url(self, url: str):
        if url.startswith('/ox/4.0/'):
            return 'https://' + self.api_hostname + url
        else:
            if url.startswith('/'):
                return 'https://' + self.api_hostname + '/ox/4.0/' + url[1:]
        return url

    @wrap_rest_method
    def get(self, url, params=None, **kwargs):
        """Sends a GET request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.get(url, params=params, **kwargs)

    @wrap_rest_method
    def options(self, url, **kwargs):
        """Sends a OPTIONS request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.options(url, **kwargs)

    @wrap_rest_method
    def head(self, url, **kwargs):
        """Sends a HEAD request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.head(url, **kwargs)

    @wrap_rest_method
    def post(self, url, data=None, json=None, **kwargs):
        """Sends a POST request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.post(url, data=data, json=json, **kwargs)

    @wrap_rest_method
    def put(self, url, data=None, **kwargs):
        """Sends a PUT request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.put(url, data=data, **kwargs)

    @wrap_rest_method
    def delete(self, url, **kwargs):
        """Sends a DELETE request, adding session cookie with token.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        return requests.delete(url, **kwargs)
