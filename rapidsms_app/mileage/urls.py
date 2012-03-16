from .views import *

urlpatterns = CarCRUDL().as_urlpatterns()
urlpatterns += MileageReportCRUDL().as_urlpatterns()
