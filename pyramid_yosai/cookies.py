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
        self.set_cookie_attributes = {} # TBD

    @property
    def remember_me(self):
        return self._get_cookie('remember_me', self.secret)

    @remember_me.setter
    def remember_me(self, rememberme):
        cookie = {'value': rememberme}
        cookie.update(self.set_cookie_attributes)
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
        cookie.update(self.set_cookie_attributes)
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

    def _set_cookie(self, response, cookie_name, cookie_val, cookie_max_age,
                    cookie_path, cookie_domain, cookie_secure, cookie_httponly,
                    secret):
        cookieval = signed_serialize(cookie_val, secret)
        response.set_cookie(
            cookie_name,
            value=cookieval,
            max_age=cookie_max_age,
            path=cookie_path,
            domain=cookie_domain,
            secure=cookie_secure,
            httponly=cookie_httponly,
            )


    def _delete_cookie(response, cookie_name, cookie_path, cookie_domain):
        response.delete_cookie(cookie_name, path=cookie_path, domain=cookie_domain)


    def _cookie_callback(
        request,
        response,
        session_cookie_was_valid,
        cookie_on_exception,
        set_cookie,
        delete_cookie,
        ):
        """Response callback to set the appropriate Set-Cookie header."""
        session = request.session
        if session._invalidated:
            if session_cookie_was_valid:
                delete_cookie(response=response)
            return
        if session.new:
            if cookie_on_exception is True or request.exception is None:
                set_cookie(request=request, response=response)
            elif session_cookie_was_valid:
                # We don't set a cookie for the new session here (as
                # cookie_on_exception is False and an exception was raised), but we
                # still need to delete the existing cookie for the session that the
                # request started with (as the session has now been invalidated).
                delete_cookie(response=response)
