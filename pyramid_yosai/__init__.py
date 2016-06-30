from pyramid.tweens import EXCVIEW


def register_yosai(config, yosai):

    def callback():
        config.registry['yosai'] = yosai

    discriminator = ('register_yosai',)
    config.action(discriminator, callable=callback)


def includeme(config):  # pragma: no cover
    """
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_directive('register_yosai', register_yosai)

    config.add_tween('pyramid_yosai.tweens.yosai_subject_tween_factory', over=EXCVIEW)

    config.add_request_method(lambda request: request.subject, 'subject', reify=False)

    config.add_request_method(lambda request: request.subject.get_session(),
                              'session', reify=False)
