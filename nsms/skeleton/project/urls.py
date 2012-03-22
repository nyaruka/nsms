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



