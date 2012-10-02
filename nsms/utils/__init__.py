from django.contrib.auth.models import User, Group
from django.conf import settings
import sys

def import_from_string(kls):
    """
    Used to load a class object dynamically by name
    """
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m

def get_sms_profile(connection):
    """
    Given a connection, looks up the SMS profile using the SMS_PROFILE model registered in settings.py
    """
    profile_class_name = getattr(settings, 'SMS_PROFILE', None)

    # no SMS_PROFILE set, then return nothing
    if not profile_class_name:
        return None

    profile_class = import_from_string(profile_class_name)

    # see if we can find a match for that connection
    matches = profile_class.objects.filter(connection=connection)
    if matches:
        return matches[0]

    else:
        return None

def get_connection_user(connection):
    """
    Gets o user for the passed in connection, creating it if necessary.  This will go ahead and create
    a special group of "SMS Users" if one is not already present.  The username will be in the format:
           [backend_name]_[phone_number]
    """
    username = "%s_%s" % (connection.backend.name, connection.identity)

    (sms_users, created) = Group.objects.get_or_create(name="SMS Users")
    existing = User.objects.filter(username=username)

    if not existing:
        user = User.objects.create_user(username)
        user.groups.add(sms_users)

    else:
        user = existing[0]

    return user
        

    
    
    
