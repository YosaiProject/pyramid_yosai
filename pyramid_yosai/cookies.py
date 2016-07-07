import functools

from pyramid.session import (
    signed_deserialize,
    signed_serialize,
)

from yosai.web import (
    web_abcs
)


class PyramidWebRegistry(web_abcs.WebRegistry):

    def __init__(self, request, secret):
        self.request = request
        self.secret = secret
        self.cookies = {'set_cookie': {}, 'delete_cookie': set()}
        self.request.add_response_callback(self.webregistry_callback)
        self._session_creation_enabled = True
        self.set_cookie_attributes = {}  # TBD

    @property
    def remember_me(self):
        return self._get_cookie('remember_me', self.secret)

    @remember_me.setter
    def remember_me(self, rememberme):
        cookie = {'value': rememberme}
        self.cookies['set_cookie']['remember_me'] = cookie

    @remember_me.deleter
    def remember_me(self):
        self.cookies['delete_cookie'].add('remember_me')

    @property
    def session_id(self):
        return self._get_cookie('session_id', self.secret)

    @session_id.setter
    def session_id(self, session_id):
        cookie = {'value': session_id}
        self.cookies['set_cookie']['session_id'] = cookie

    @session_id.deleter
    def session_id(self):
        self.cookies['delete_cookie'].add('session_id')

    @property
    def remote_host(self):
        return self.request.client_addr

    @property
    def session_creation_enabled(self):
        return self._session_creation_enabled

    @session_creation_enabled.setter
    def session_creation_enabled(self, session_creation_enabled):
        self._session_creation_enabled = session_creation_enabled

    @session_creation_enabled.deleter
    def session_creation_enabled(self):
        self._session_creation_enabled = None

    def webregistry_callback(self, request, response):
        while self.cookies['set_cookie']:
            key, value = self.cookies['set_cookie'].popitem()
            self._set_cookie(response, key, **value)

        while self.cookies['delete_cookie']:
            key = self.cookies['delete_cookie'].pop()
            self._delete_cookie(response, key)

    def _get_cookie(self, cookie_name, secret):
        cookie = self.request.cookies.get(cookie_name)

        try:
            return signed_deserialize(cookie, secret)
        except (ValueError, AttributeError):
            return None

    def _set_cookie(self, response, cookie_name, cookie_val):

        cookieval = signed_serialize(cookie_val, self.secret)

        response.set_cookie(
            cookie_name,
            value=cookieval,
            max_age=self.set_cookie_attributes.get('cookie_max_age', None),
            path=self.set_cookie_attributes.get('cookie_path', None),
            domain=self.set_cookie_attributes.get('cookie_domain', None),
            secure=self.set_cookie_attributes.get('cookie_secure', None),
            httponly=self.set_cookie_attributes.get('cookie_httponly', None))

    def _delete_cookie(self, response, cookie_name):

        response.delete_cookie(
            cookie_name,
            path=self.set_cookie_attributes.get('cookie_path', None),
            domain=self.set_cookie_attributes.get('cookie_domain', None))
