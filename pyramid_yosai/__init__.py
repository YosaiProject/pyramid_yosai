from pyramid.tweens import EXCVIEW


def set_yosai(config, yosai):

    def callback():
        config.registry['yosai'] = yosai

    discriminator = ('register_yosai',)
    config.action(discriminator, callable=callback)


def _parse_settings(settings):
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
    pass


def create_yosai_from_settings(settings):
    """
    Convenience method to construct a ``Yosai`` instance from Paste config
    settings. Only settings prefixed with "yosai." are inspected
    and, if needed, coerced to their appropriate types (for example, casting
    the ``timeout`` value as an `int`).

    :param settings: A dict of Pyramid application settings
    :returns: a Yosai instance
    """
    security_manager = _parse_settings(settings)
    pass


def includeme(config):  # pragma: no cover
    """
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_directive('register_yosai', set_yosai)

    config.add_tween('pyramid_yosai.tweens.pyramid_yosai_tween_factory',
                     over=EXCVIEW)

    config.add_request_method(lambda request: request.subject.get_session(),
                              'session',
                              reify=False)
