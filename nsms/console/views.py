from smartmin.views import *
from rapidsms_httprouter.models import Message
from rapidsms_httprouter.router import get_router
from django.utils.safestring import mark_safe

class MessageTesterForm(forms.Form):
    sender = forms.CharField(max_length=20, initial="12065551212")
    text = forms.CharField(max_length=160, label="Message", widget=forms.TextInput(attrs={'size':'60'}))

class MessageCRUDL(SmartCRUDL):
    actions = ('list', 'csv')
    model = Message
    permissions = True

    class Csv(SmartCsvView):
        fields = ('date', 'direction', 'number', 'text',)

        def get_number(self, obj):
            return obj.connection.identity

    class List(SmartListView, SmartFormMixin):
        title = "Message Console"

        fields = ('direction', 'number', 'text', 'date')
        default_order = ('-date',)
        search_fields = ('text', 'connection__identity__icontains')
        field_config = { 'direction': dict(label=" ") }

        refresh = 5000

        def post(self, *args, **kwargs):
            # valid form, then process the message
            form = MessageTesterForm(self.request.POST)
            if form.is_valid():
                message = get_router().handle_incoming('console',
                                                       form.cleaned_data['sender'],
                                                       form.cleaned_data['text'])                


            # and off we go
            self.object_list = self.get_queryset()
            context = self.get_context_data(object_list=self.object_list)

            return self.render_to_response(context)
        
        def get_context_data(self, **kwargs):
            context = super(MessageCRUDL.List, self).get_context_data(**kwargs)
            
            if self.request.method == 'POST':
                context['form'] = MessageTesterForm(self.request.POST)
            else:
                context['form'] = MessageTesterForm()
            return context
        
        def get_number(self, obj):
            return obj.connection.identity

        def get_direction(self, obj):
            if obj.direction == 'I':
                if obj.connection.backend.name == 'console':
                    style = 'cin'
                else:
                    style = 'in'
            else:
                if obj.connection.backend.name == 'console':
                    style = 'cout'
                elif obj.status == 'D':
                    style = 'delivered'
                elif obj.status == 'S' or obj.connection.backend.name == 'console':
                    style = 'sent'
                else:
                    style = 'queued'

            return mark_safe('<div class="%s"> </div>' % style)
                
