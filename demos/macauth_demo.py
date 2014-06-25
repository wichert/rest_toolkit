

import random
import wsgiref.simple_server

from pyramid.config import Configurator
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.exceptions import Forbidden

from pyramid_macauth import MACAuthenticationPolicy


TEMPLATE = """
Hello {userid}!
Your lucky number for today is {number}.
"""

 
def lucky_number(request):
    """Pyramid view to generate a lucky number."""

    # Check that the user is authenticated.
    userid = authenticated_userid(request)
    if userid is None:
        raise Forbidden()

    # Generate and return the lucky number.
    number = random.randint(1,100)
    return Response(TEMPLATE.format(**locals()), content_type="text/plain")


def provision_creds(request):
    """Pyramid view to provision MACAuth credentials."""

    # Check that the user is authenticated.
    userid = authenticated_userid(request)
    if userid is None:
        raise Forbidden()

    # Get a reference to the MACAuthenticationPolicy plugin.
    policy = request.registry.getUtility(IAuthenticationPolicy)
    policy = policy.get_policy(MACAuthenticationPolicy)
    
    # Generate a new id and secret key for the current user.
    id, key = policy.encode_mac_id(request, userid)
    return {"id": id, "key": key}
 

def main():
    """Construct and return a WSGI app for the luckynumber service."""

    settings = {
      # The pyramid_persona plugin needs a master secret to use for
      # signing login cookies, and the expected hostname of your website
      # to prevent fradulent login attempts.
      "persona.secret": "TED KOPPEL IS A ROBOT",
      "persona.audiences": "localhost:8080",

      # The pyramid_macauth plugin needs a master secret to use for signing
      # its access tokens.  We could use the same secret as above, but it's
      # generally a good idea to use different secrets for different things.
      "macauth.master_secret": "V8 JUICE IS 1/8TH GASOLINE",

      # The pyramid_multiauth plugin needs to be told what sub-policies to
      # load, and the order in which they should be tried.
      "multiauth.policies": "pyramid_persona pyramid_macauth",
    }

    config = Configurator(settings=settings)
    config.add_route("number", "/")
    config.add_view(lucky_number, route_name="number")

    # Including pyramid_multiauth magically enables authentication, loading
    # both of the policies we specified in the settings.
    config.include("pyramid_multiauth")

    # Both of our chosen policies configure a "forbidden view" to handle
    # unauthenticated access.  We have to resolve this conflict by explicitly
    # picking which one we want to use.
    config.add_forbidden_view("pyramid_persona.views.forbidden")

    config.add_route("provision", "/provision")
    config.add_view(provision_creds, route_name="provision", renderer="json")

    return config.make_wsgi_app()


if __name__ == "__main__":
    app = main()
    server = wsgiref.simple_server.make_server("", 8081, app)
    server.serve_forever()

