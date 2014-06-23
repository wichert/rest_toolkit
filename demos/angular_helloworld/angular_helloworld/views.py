from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('angular_helloworld')

def my_view(request):
    return {'project':'angular_helloworld'}
