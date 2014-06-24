from pyramid.config import Configurator
from .models import get_root

def main(global_config, **settings):
    settings = dict(settings)

    config = Configurator(root_factory=get_root, settings=settings)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')
    config.scan(".")

    return config.make_wsgi_app()
