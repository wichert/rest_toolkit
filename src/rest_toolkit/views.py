from pyramid.httpexceptions import HTTPMethodNotAllowed
from pyramid.httpexceptions import HTTPNoContent
from .state import RestState


def unsupported_method_view(resource, request):
    request.response.status_int = 405
    return {'message': 'Unsupported HTTP method'}


def default_options_view(resource, request, methods=None):
    """Default OPTIONS view for resources."""
    response = HTTPNoContent()
    if methods is None:
        state = RestState.from_resource(resource)
        methods = state.supported_methods()
    response.headers['Access-Control-Allow-Methods'] = ', '.join(methods)
    return response


def default_delete_view(resource, request):
    resource.delete()
    return HTTPNoContent()


def default_get_view(resource, request):
    return resource.to_dict()


def default_patch_view(resource, request):
    try:
        data = request.json_body
    except ValueError:
        request.response.status_int = 400
        return {'message': 'No JSON data provided.'}
    resource.validate(data, partial=True)
    r = resource.update_from_dict(data, replace=False)
    return r if r is not None else resource.to_dict()


def default_put_view(resource, request):
    try:
        data = request.json_body
    except ValueError:
        request.response.status_int = 400
        return {'message': 'No JSON data provided.'}
    resource.validate(data, partial=False)
    r = resource.update_from_dict(data, replace=True)
    return r if r is not None else resource.to_dict()


def default_post_view(resource, request):
    try:
        data = request.json_body
    except ValueError:
        request.response.status_int = 400
        return {'message': 'No JSON data provided.'}
    resource.validate_child(data)
    request.response.status_int = 201
    return resource.add_child(data)
