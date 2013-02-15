from smartmin.views import *
from rapidsms.models import Backend
from rapidsms_httprouter.models import Message
from rapidsms_httprouter.router import get_router
from django.utils.safestring import mark_safe
from django.db.models import Count
import datetime

class MessageTesterForm(forms.Form):
    sender = forms.CharField(max_length=20, initial="12065551212")
    text = forms.CharField(max_length=160, label="Message", widget=forms.TextInput(attrs={'size':'60'}))

class MessageCRUDL(SmartCRUDL):
    actions = ('list', 'csv', 'monthly')
    model = Message
    permissions = True

    class Csv(SmartCsvView):
        fields = ('date', 'direction', 'number', 'text')

        def get_number(self, obj):
            return obj.connection.identity

        def derive_queryset(self, **kwargs):
            # get our parent queryset
            queryset = super(MessageCRUDL.Csv, self).derive_queryset(**kwargs)

            # return our queryset
            return queryset.select_related(depth=1)

    class Status(SmartListView):
        permission = None

        def get_context_data(self, *args, **kwargs):
            context = super(MessageCRUDL.Status, self).get_context_data(*args, **kwargs)

            # get all messages that are unset for more than 30 seconds
            thirty_seconds_ago = datetime.datetime.now() - datetime.timedelta(seconds=30)
            context['unsent'] = Message.objects.filter(date__lte=thirty_seconds_ago, status='Q').count()
            context['error'] = Message.objects.filter(date__lte=thirty_seconds_ago, status='E').count()

            return context

    class Monthly(SmartListView):
        title = "Monthly Message Volume"

        def build_monthly_counts(self, objects, **filters):
            counts = objects.filter(**filters).order_by('date').extra({'month':"month(date)", 'year':"year(date)"}).values('month', 'year').annotate(created_on_count=Count('id'))
            
            for count in counts:
                count['created'] = datetime.datetime(day=1, month=count['month'], year=count['year'])

            return counts

        def get_context_data(self, **kwargs):
            context = super(MessageCRUDL.Monthly, self).get_context_data(**kwargs)
            
            # get our queryset
            objects = self.derive_queryset().order_by('date')

            # break it up by date counts
            context['incoming_counts'] = self.build_monthly_counts(objects, direction='I')
            context['outgoing_counts'] = self.build_monthly_counts(objects, direction='O')

            # build our breakdown
            month = objects[0].date.month
            year = objects[0].date.year

            start = datetime.datetime(day=1, month=month, year=year)
            today = datetime.datetime.now()
            
            counts = []
            while start < today:
                if month == 12: 
                    month = 1; year += 1
                else:
                    month += 1

                end = datetime.datetime(day=1, month=month, year=year)

                incoming_count = objects.filter(date__gte=start, date__lt=end, direction='I').count()
                outgoing_count = objects.filter(date__gte=start, date__lt=end, direction='O').count()
                total = incoming_count + outgoing_count

                counts.append(dict(start=start, incoming=incoming_count, outgoing=outgoing_count, total=total))
                start = end

            context['counts'] = counts

            return context

    class List(SmartListView, SmartFormMixin):
        title = "Message Console"

        fields = ('direction', 'number', 'text', 'date')
        default_order = '-date'
        search_fields = ('text__icontains', 'connection__identity__icontains')
        field_config = { 'direction': dict(label=" ") }

        refresh = 5000

        def derive_queryset(self, *args, **kwargs):
            queryset = super(MessageCRUDL.List, self).derive_queryset(*args, **kwargs)

            # filter by backend id if there is one in our request
            backend_id = int(self.request.REQUEST.get('backend_id', 0))
            if backend_id:
                queryset = queryset.filter(connection__backend=backend_id)

            return queryset

        def post(self, *args, **kwargs):
            # valid form, then process the message
            form = MessageTesterForm(self.request.POST)
            if form.is_valid():
                message = get_router().handle_incoming('console',
                                                       form.cleaned_data['sender'],
                                                       form.cleaned_data['text'])                

            # and off we go
            return self.get(*args, **kwargs)

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

            context['backends'] = Backend.objects.all()
            context['backend_id'] = int(self.request.REQUEST.get('backend_id', 0))

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
                
