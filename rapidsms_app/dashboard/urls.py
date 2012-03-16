from django.conf.urls.defaults import patterns, include, url
from .views import index, status

urlpatterns = urlpatterns = patterns('',
   url(r'^$', index, name='dashboard'),
   url(r'^status$', status, name='status'),
)
