from pyramid.tweens import EXCVIEW
from pyramid.path import DottedNameResolver

from yosai.core import AccountStoreRealm
from yosai.web import WebSecurityManager, WebYosai
from yosai_dpcache.cache import DPCacheHandler
from yosai_alchemystore import AlchemyAccountStore

from marshmallow import Schema, fields

from .forms import YosaiForm, LoginForm  # required by 3rd party


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
    Convenience method to construct a ``Yosai`` instance, referencing paste-deploy
    INI settings to obtain the envvar or filepath to yosai settings.

    :raises: KeyError when neither yosai env_var nor file_path are defined
    :returns: a Yosai instance
    """
    env_var = settings['yosai.settings_filepath_envvar']
    if env_var:
        return WebYosai(env_var=env_var)

    file_path = settings['yosai.settings_filepath']
    if file_path:
        return WebYosai(file_path=file_path)

    raise ValueError('pyramid_yosai must have either an env_var or file_path')


def includeme(config):  # pragma: no cover
    """
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_directive('set_yosai', set_yosai)

    config.add_tween('pyramid_yosai.tweens.pyramid_yosai_tween_factory',
                     over=EXCVIEW)

    yosai = yosai_from_settings(config.registry.settings)
    if yosai:
        config.registry['yosai'] = yosai
