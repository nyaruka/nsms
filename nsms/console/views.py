from smartmin.views import *
from rapidsms_httprouter.models import Message
from rapidsms_httprouter.router import get_router
from django.utils.safestring import mark_safe
from django.db.models import Count
import datetime

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

        def derive_queryset(self, **kwargs):
            # get our parent queryset
            queryset = super(MessageCRUDL.Csv, self).derive_queryset(**kwargs)

            # return our queryset
            return queryset.select_related(depth=1)

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

        def build_daily_counts(self, objects, **filters):
            counts = objects.filter(**filters).order_by('date').extra({'created':"date(date)"}).values('created').annotate(created_on_count=Count('id'))
            
            for count in counts:
                created_str = count['created']
                if not hasattr(created_str, 'year'):
                    count['created'] = datetime.datetime.strptime(created_str, "%Y-%m-%d")

            return counts
        
        def get_context_data(self, **kwargs):
            context = super(MessageCRUDL.List, self).get_context_data(**kwargs)
            
            # get our queryset
            objects = self.derive_queryset()
            one_month = datetime.datetime.now() - datetime.timedelta(days=30)

            # break it up by date counts
            context['incoming_counts'] = self.build_daily_counts(objects, direction='I', date__gte=one_month)
            context['outgoing_counts'] = self.build_daily_counts(objects, direction='O', date__gte=one_month)

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
                
