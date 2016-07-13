from yosai.core import get_current_subject
import wtforms
from wtforms.ext.csrf.form import SecureForm
from pyramid.exceptions import BadCSRFToken


class YosaiForm(SecureForm):

    def __init__(self, formdata=None, obj=None, prefix='', context=None,
                 **kwargs):
        super().__init__(formdata, obj, prefix, **kwargs)
        self.context = context  # a dict containing a request object
        self.csrf_token.current_token = self.generate_csrf_token(
            self.context.get('request'))
        self.obj = obj

    def generate_csrf_token(self, csrf_context):
        if not csrf_context:
            subject = get_current_subject()
            return subject.get_session().get_csrf_token()
        return csrf_context.session.get_csrf_token()

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
        filters=[strip_filter],
        validators=[
            wtforms.validators.InputRequired(),
            wtforms.validators.Length(min=3),
            wtforms.validators.EqualTo('confirm', message='Passwords must match')
        ])

    confirm = wtforms.PasswordField('Repeat password')
