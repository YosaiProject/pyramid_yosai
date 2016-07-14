from pyramid.tweens import EXCVIEW

from yosai.core import AccountStoreRealm
from yosai.web import WebSecurityManager, WebYosai
from yosai_dpcache.cache import DPCacheHandler
from yosai_alchemystore import AlchemyAccountStore

from marshmallow import Schema, fields

from .forms import (
    LoginForm,
)


def set_yosai(config, yosai):
    """
    Use config.set_yosai when you want to manually set the Yosai instance in
    Pyramid's registry rather than initialize Yosai from INI config, as
    performed by _create_yosai_from_settings.
    """

    def callback():
        config.registry['yosai'] = yosai

    discriminator = ('set_yosai',)
    config.action(discriminator, callable=callback)


def _parse_security_manager_settings(settings):
    """
    Currently, Yosai can be configured from settings specified within pyramid
    settings INI file in conjunction with settings files specific to Yosai,
    namely:
        - YOSAI_CORE_SETTINGS
        - YOSAI_CACHE_SETTINGS
        - YOSAI_ALCHEMYSTORE_SETTINGS

    yosai.accountstore
    yosai.realms = {class: store}
    """

    # this is a temporary, hard-coded solution until INI parsing is finished

    class AttributesSchema(Schema):
        test = fields.String()

    realm = AccountStoreRealm(account_store=AlchemyAccountStore())

    return WebSecurityManager(realms=(realm,),
                              cache_handler=DPCacheHandler(),
                              session_attributes_schema=AttributesSchema)


def yosai_from_settings(settings):
    """
    Convenience method to construct a ``Yosai`` instance from Paste config
    settings. Only settings prefixed with "yosai." are inspected
    and, if needed, coerced to their appropriate types (for example, casting
    the ``timeout`` value as an `int`).

    :param settings: A dict of Pyramid application settings
    :returns: a Yosai instance
    """
    try:
        security_manager = _parse_security_manager_settings(settings)
        return WebYosai(security_manager)
    except AttributeError:
        return None


def includeme(config):  # pragma: no cover
    """
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_directive('set_yosai', set_yosai)

    config.add_tween('pyramid_yosai.tweens.pyramid_yosai_tween_factory',
                     over=EXCVIEW)

    # config.add_request_method(lambda request: Yosai.get_current_subject().get_session(),
    #                           'session',
    #                          reify=False)

    yosai = yosai_from_settings(config.registry.settings)
    if yosai:
        config.registry['yosai'] = yosai
