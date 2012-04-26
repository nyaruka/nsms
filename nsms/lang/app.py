from rapidsms.apps.base import AppBase
from nsms.parser import Parser
from nsms.text.models import gettext as _
from nsms.utils import get_sms_profile
from django.conf import settings
from django.utils import translation
import re

# hackery to make sure our translation database contains all our the strings used in this app
_('lang-current-lang', "Your language is set to {{ language }}.")
_('lang-unknown-language', "Sorry, the language code '{{ code }}' is not supported.")
_('lang-set-success', "Success, your language is now set to {{ language }}.")

class App(AppBase):
    """
    This app is responsible for setting and changing a user's preferred language.

    In order for this app to do it's magic, you need to define what your SMS profile in 
    your settings_common.py:

           SMS_PROFILE = 'chws.chw'

    The language app will respond to messages that begin with the keyword 'lang'.  Without
    an argument it will respond with the currently selected language, with an argument it
    will try to find a configured language with that name and set it, eg:

           lang en[_us]
           lang rw
    """
    def handle (self, message):
        profile = get_sms_profile(message.connection)

        # handle activating the appropriate SMS language

        # if this connection has a profile, use that language
        if profile:
            translation.activate(profile.language)

        # otherwise use the default SMS language
        else:
            translation.activate(settings.DEFAULT_SMS_LANGUAGE)

        parser = Parser(message.text)

        # check whether this is a lang message
        keyword = parser.next_keyword(['lang'])
        if keyword:
            if not profile:
                message.respond(_('lang-unknown-user', "Sorry, your phone number is not registered."))
                return True

            # just querying the language
            language = parser.next_word()
            if not language:
                message.respond(_('lang-current-lang', "Your language is set to {{ language }}.", dict(language=profile.get_language_display())))
                return True

            else:
                # lowercase the language they passed us
                language = language.lower()

                lang_mapping = dict()
                for lang in settings.LANGUAGES:
                    code = lang[0].lower()
                    lang_mapping[code] = code

                    parts = code.split('_')
                    if not parts[0] in lang_mapping:
                        lang_mapping[parts[0]] = code

                # this language doesn't exit
                if not language.lower() in lang_mapping:
                    message.respond(_('lang-unknown-language', "Sorry, the language code '{{ code }}' is not supported.", dict(code=language.lower())))
                    return True

                profile.language = lang_mapping[language.lower()]
                profile.save()
                
                # activate the new language
                translation.activate(profile.language)
                message.respond(_('lang-set-success', "Success, your language is now set to {{ language }}.", dict(language=profile.get_language_display())))

                return True

        return False


                    


