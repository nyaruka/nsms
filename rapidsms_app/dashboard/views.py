from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from smartmin.views import *
from django import forms
from django.contrib.auth.decorators import login_required
from rapidsms_httprouter.models import Message
from rapidsms.models import Backend
from django.conf import settings

@login_required
def index(request):
    context = dict()
    return render_to_response('dashboard/index.html', context, context_instance=RequestContext(request))

def status(request):
    (backend, created) = Backend.objects.get_or_create(name=settings.DEFAULT_BACKEND)
    unsent_count = Message.objects.filter(status__in=['L','Q'], connection__backend=backend).count()
    if unsent_count > 1:
        return HttpResponse("ERROR - UNSENT COUNT: %s" % unsent_count)
    else:
        return HttpResponse("OK")
