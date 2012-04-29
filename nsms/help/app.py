from rapidsms.apps.base import AppBase
from nsms.text import gettext as _
import re

_('help', "Unrecognized message, please contact your supervisor for more information")

class App(AppBase):
    """
    This app is responsible for returning a help message for any message which reaches it.  This makes
    sense for applications which have a shortcode dedicated to them.
    """
    def handle (self, message):
        return message.respond(_('help',
                                 "Unrecognized message, please contact your supervisor for more information"))
