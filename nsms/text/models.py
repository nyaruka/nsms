from django.db import models
from smartmin.models import SmartModel

class Text(SmartModel):
    slug = models.SlugField(unique=True,
                            help_text="The unique word used to identify this piece of text")
    text = models.CharField(max_length=200, 
                            help_text="The text that will be displayed to the user for this language")
