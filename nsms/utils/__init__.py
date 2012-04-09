from django.contrib.auth.models import User, Group

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
        

    
    
    
