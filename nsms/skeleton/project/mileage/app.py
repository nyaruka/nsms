from rapidsms.apps.base import AppBase
from .models import *
from nsms.text.models import gettext as _
from nsms.parser import Parser, ParseException
from rapidsms.models import Backend, Connection
from django.utils import translation
from rapidsms_httprouter.router import get_router
from django.template import Template, Context
from django.conf import settings
import re

KEYWORDS = [ 'm', 'miles', 'c', 'car' ]

_('unrecognized', "That message is not recognized, must start with miles or car")
_('car-invalid-license', "Invalid license plate, it must be 8 letters")
_('car-add-success', "You are now reporting mileage for the car with license {{ license_plate }}")
_('bad-car-format', "Error, car message must take the form: car [license plate]")

_('miles-no-car', "You are not registered to be using a car, send: car [license plate] to register")
_('miles-success', "You have recorded {{ miles }} for the car with license {{ license_plate }}")
_('bad-miles-format', "Error, mileage reports must take the form: miles [mileage]")

_('error', "An unexpected error occurred, please check your message and try again")

class App(AppBase):
    
    def handle (self, message):
        # activate our default language
        translation.activate(settings.DEFAULT_SMS_LANGUAGE)

        # if the number looks like something informational or SPAM, ignore
        identity = message.connection.identity

        # first case, alpha num identity
        try:
            number = int(identity)
        except:
            # ignore this message, the sender isn't numeric
            return False

        # now test that it is 10 digits or more, ignore anything shorter
        if len(identity) < 10:
            return False

        # ok sender looks ok, let's get on with it

        try:
            response = self.handle_message(message)

            if response:
                message.respond(response)
            else: # pragma: no cover
                message.respond(_('unrecognized', "That message is not recognized, must start with miles or car"))

        except ParseException as e:
            message.respond(str(e))

        except:
            import traceback
            traceback.print_exc()
            message.respond(_('error', "An unexpected error occurred, please check your message and try again"))

        return True

    def handle_message(self, message):
        """
        Messages have the following keywords:
            'miles' or 'car'
        """
        parser = Parser(message.text)
        keyword = parser.next_keyword(KEYWORDS, _('unrecognized', "That message is not recognized, must start with miles or car"))

        if keyword in ['car', 'c']:
            return self.handle_car(message, parser)

        elif keyword in ['miles', 'm']:
            return self.handle_miles(message, parser)

    def handle_car(self, message, parser):
        bad_format = _('bad-car-format', "Error, car message must take the form: car [license plate]")
        
        license_plate = parser.next_word(bad_format)

        if len(license_plate) != 8:
            raise ParseException(_('car-invalid-license', "Invalid license plate, it must be 8 letters"))

        # otherwise, associate this connection and car
        car = Car.register_connection(license_plate, message.connection)
        return _('car-add-success', "You are now reporting mileage for the car with license {{ license_plate }}", dict(license_plate=car.license_plate))
        
    def handle_miles(self, message, parser):
        bad_format = _('bad-miles-format', "Error, mileage report message must take the form: miles [mileage]")
        miles = parser.next_int(bad_format)

        # look up whether this connection has a car
        car = Car.for_connection(message.connection)
        if not car:
            _('miles-no-car', "You are not registered to be using a car, send: car [license plate] to register")

        # add mileage
        car.add_mileage(miles, message.connection)

        return _('miles-success', "You have recorded {{ miles }} miles for the car with license {{ license_plate }}", dict(miles=miles, license_plate=car.license_plate))
        



