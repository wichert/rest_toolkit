class DemoSite(object):
    title = "AngularJs Todo Demo"

root = DemoSite()


def get_root(request):
    return root
