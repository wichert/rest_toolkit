from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import unauthenticated_userid


def generic(context, request):
    request.response.status_int = 500
    try:
        return {'message': unicode(message)}
    except NameError:  # pragma: nocov
        # Python 3.x has no unicode()
        return {'message': str(message)}


def notfound(context, request):
    message = 'Resource not found'
    if isinstance(context, HTTPNotFound):
        if context.content_type == 'application/json':
            return context
        elif context.detail:
            message = context.detail
    request.response.status_int = 404
    return {'message': message}


def forbidden(request):
    if unauthenticated_userid(request):
        request.response.status_int = 403
        return {'message': 'You are not allowed to perform this action.'}
    else:
        request.response.status_int = 401
        return {'message': 'You must login to perform this action.'}
