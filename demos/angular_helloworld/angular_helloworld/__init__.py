from pyramid.config import Configurator
from angular_helloworld.models import get_root

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    settings = dict(settings)

    config = Configurator(root_factory=get_root, settings=settings)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')
    config.add_view('angular_helloworld.views.my_view',
                    context='angular_helloworld.models.MyModel', 
                    renderer="templates/mytemplate.jinja2")

    return config.make_wsgi_app()
