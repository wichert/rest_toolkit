from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import unauthenticated_userid


def generic(context, request):
    request.response.status_int = 500
    try:
        return {'message': context.args[0]}
    except IndexError:
        return {'message': 'Unknown error'}


def http_error(context, request):
    request.response.status = context.status
    for (header, value) in context.headers.items():
        if header in {'Content-Type', 'Content-Length'}:
            continue
        request.response.headers[header] = value
    if context.message:
        return {'message': context.message}
    else:
        return {'message': context.status}


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
