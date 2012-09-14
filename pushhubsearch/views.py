from pyramid.view import view_config
from .models import Root


@view_config(context=Root, renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'push-hubsearch'}
