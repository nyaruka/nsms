from rapidsms.apps.base import AppBase
import re

class App(AppBase):
    """
    This app is responsible for filtering out messages that seem to be coming from short codes, 
    as these are usually SPAM in one way or another.
    """
    
    def handle (self, message):
        # if the number looks like something informational or SPAM, ignore
        identity = message.connection.identity

        # first case, alpha num identity
        try:
            number = int(identity)
        except:
            # ignore this message, the sender isn't numeric
            return True

        # now test that it is 10 digits or more, ignore anything shorter
        if len(identity) < 10:
            return True

        # look ok, let another app handle this message
        return False
