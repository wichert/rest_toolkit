from pyramid.config import Configurator
from .models import get_root


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization'
        })

    event.request.add_response_callback(cors_headers)


from pyramid.events import NewRequest


def main(global_config, **settings):
    settings = dict(settings)

    config = Configurator(root_factory=get_root, settings=settings)
    config.scan(".")

    config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    return config.make_wsgi_app()
