from django.db import models
from smartmin.models import SmartModel
from django.contrib.auth.models import User
from django.template import Template, Context

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
        # our text is a template, perform substitutions on it
        template = Template("%s" % text)
        return template.render(Context(variables))

class Text(SmartModel):
    slug = models.SlugField(unique=True,
                            help_text="The unique word used to identify this piece of text")
    text = models.CharField(max_length=160, 
                            help_text="The text that will be displayed to the user for this language")
