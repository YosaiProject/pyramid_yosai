from pyramid.session import (
    signed_deserialize,
    signed_serialize,
)

from yosai.web import (
    web_abcs
)


class PyramidWebRegistry(web_abcs.WebRegistry):

    def __init__(self, request, secret='changeme'):
        super().__init__(request, secret)

    def register_response_callback(self):
        self.request.add_response_callback(self.webregistry_callback)

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
