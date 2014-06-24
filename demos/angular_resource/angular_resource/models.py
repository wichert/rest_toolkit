class DemoSite(object):
    title = "AngularJs Todo Demo"


def get_root(request):
    root = DemoSite()

    return root
