import wtforms

from yosai.web import WebYosai
from wtforms.ext.csrf.form import SecureForm
from pyramid.exceptions import BadCSRFToken


class YosaiForm(SecureForm):

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super().__init__(formdata, obj, prefix, **kwargs)
        self.csrf_token.current_token = self.generate_csrf_token()
        self.obj = obj

    def generate_csrf_token(self, context=None):
        # the context param isn't needed with yosai
        subject = WebYosai.get_current_subject()
        session = subject.get_session()
        return session.get_csrf_token()

    def validate_csrf_token(self, field):
        if field.data != field.current_token:
            raise BadCSRFToken()


def strip_filter(value):
    return value.strip() if value else None


class LoginForm(YosaiForm):
    username = wtforms.StringField(
        "Username",
        filters=[strip_filter],
        validators=[wtforms.validators.InputRequired(),
                    wtforms.validators.Length(min=3)])

    password = wtforms.PasswordField(
        "Password",
        validators=[
            wtforms.validators.InputRequired(),
            wtforms.validators.Length(min=3),
        ])

    remember_me = wtforms.BooleanField('Remember Me', default=False)
