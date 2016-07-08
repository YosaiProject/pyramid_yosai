from yosai.core import get_current_subject
from wtforms.ext.csrf.form import SecureForm
from pyramid.exceptions import BadCSRFToken


class YosaiForm(SecureForm):

    def __init__(self, formdata=None, obj=None, prefix='', context=None,
                 **kwargs):
        super().__init__(formdata, obj, prefix, **kwargs)
        self.context = context
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
