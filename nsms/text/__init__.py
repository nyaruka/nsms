from django.contrib.auth.models import User
from django.template.base import Template
from django.template.context import Context
from nsms.text.models import Text

def gettext(slug, default_string, variables=None):
    text = Text.objects.filter(slug=slug)

    if text:
        text = text[0].text
    else:
        Text.objects.create(slug=slug,
            text=default_string,
            created_by=User.objects.get(id=-1),
            modified_by=User.objects.get(id=-1))
        text = default_string

    if variables is None:
        return text
    else:
        try:
            # our text is a template, perform substitutions on it
            template = Template("%s" % text)
            return template.render(Context(variables))
        except Exception as e:
            # if we throw an error, display the raw template
            return text
