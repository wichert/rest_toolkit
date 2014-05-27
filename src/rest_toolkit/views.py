from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.httpexceptions import HTTPNoContent
from .state import RestState


def unsupported_method_view(resource, request):
    return HTTPMethodNotAllowed()


def default_options_view(resource, request):
    """Default OPTIONS view for resources."""
    response = HTTPNoContent()
    state = RestState.from_resource(resource)
    response.headers['Access-Control-Allow-Methods'] = ', '.join(state.supported_methods())
    return response
