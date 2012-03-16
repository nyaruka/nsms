from django.db import models
from smartmin.models import SmartModel
from django.contrib.auth.models import User

def gettext(slug, default_string):
    text = Text.objects.filter(slug=slug)

    if text:
        return text[0].text
    else:
        text = Text.objects.create(slug=slug,
                                   text=default_string,
                                   created_by=User.objects.get(id=-1),
                                   modified_by=User.objects.get(id=-1))
        return default_string

class Text(SmartModel):
    slug = models.SlugField(unique=True,
                            help_text="The unique word used to identify this piece of text")
    text = models.CharField(max_length=160, 
                            help_text="The text that will be displayed to the user for this language")
