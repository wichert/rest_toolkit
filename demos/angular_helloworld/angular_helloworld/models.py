class DemoSite(object):
    title = "AngularJs Hello World Demo"

root = DemoSite()


def get_root(request):
    return root
