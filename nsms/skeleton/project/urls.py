from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import permission_required, login_required
from rapidsms_httprouter.views import console
from django.conf import settings

urlpatterns = patterns('',
    url(r'^users/', include('smartmin.users.urls')),
    url(r'^text/', include('nsms.text.urls')),
    url('^console/', include('nsms.console.urls')),
    url('', include('rapidsms_httprouter.urls')),

    # add your apps here
    url('', include('dashboard.urls')),
    url('^mileage/', include('mileage.urls')),
)

# site static for development
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }))
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }))

def handler500(request):
    """
    500 error handler which includes ``request`` in the context.

    Templates: `500.html`
    Context: None
    """
    from django.template import Context, loader
    from django.http import HttpResponseServerError

    t = loader.get_template('500.html') # You need to create a 500.html template.
    return HttpResponseServerError(t.render(Context({
        'request': request,
    })))




