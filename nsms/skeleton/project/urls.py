from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import permission_required, login_required
from rapidsms_httprouter.views import console

urlpatterns = patterns('',
    url(r'^users/', include('smartmin.users.urls')),
    url(r'^text/', include('nsms.text.urls')),
    url('^router/console', login_required(console, 'rapidsms_httprouter.message_list')),
    url('', include('dashboard.urls')),
    url('', include('rapidsms_httprouter.urls')),
    url('^mileage/', include('mileage.urls'))
)

