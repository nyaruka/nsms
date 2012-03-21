from smartmin.views import *
from .models import *

class CarCRUDL(SmartCRUDL):
    model = Car
    actions = ('list', 'read')
    permissions = True

class MileageReportCRUDL(SmartCRUDL):
    model = MileageReport
    actions = ('list', 'read')
    permissions = True
