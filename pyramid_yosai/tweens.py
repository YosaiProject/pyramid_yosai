
from pyramid.exceptions import ConfigurationError
from .mocks import PyramidWebRegistry


def yosai_subject_tween_factory(handler, registry):
    """
    This tween obtains the currently executing subject instance from Yosai and
    makes it available from the request object.
    """
    yosai = registry.get('yosai')
    if yosai is None:
        msg = ('You cannot register the Yosai subject tween without first '
               'registering a yosai instance by calling "config.set_yosai"')
        raise ConfigurationError(msg)

    def tween(request):
        web_registry = PyramidWebRegistry(request)

        with yosai(web_registry):
            request.subject = yosai.subject  # TBD
            response = handler(request)

        return response

    return tween
