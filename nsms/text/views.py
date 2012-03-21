from smartmin.views import *
from .models import *
from django import forms

class TextCRUDL(SmartCRUDL):
    actions = ('update', 'list')
    model = Text
    permissions = True

    class TextFieldMixin(object):

        def customize_form_field(self, name, field):
            if name.startswith("text"):
                field.widget = forms.Textarea(attrs = dict(cols=40, rows=4))

            return field

    class Create(TextFieldMixin, SmartCreateView):
        exclude = ('text', 'created_by', 'modified_by', 'is_active')

    class Update(TextFieldMixin, SmartUpdateView):
        exclude = ('slug', 'is_active', 'text', 'created_by', 'modified_by')

        def derive_title(self):
            return self.object.slug

        def derive_initial(self):
            initial = super(TextCRUDL.Update, self).derive_initial()
            
            if not initial.get('text_en_us', None):
                initial['text_en_us'] = self.object.text

            return initial

    class List(SmartListView):
        default_order = ('slug')
        fields = ('slug', 'text')

    
