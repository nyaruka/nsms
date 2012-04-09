from django.test import TestCase
from django.contrib.auth.models import User, Group
from urlparse import urlparse
from rapidsms.models import Backend, Connection
from rapidsms_httprouter.router import get_router
import datetime

class NSMSTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@admin.com', 'admin')
        self.admin.groups.add(Group.objects.get(name='Administrators'))

        self.backend = Backend.objects.create(name="test")
        self.conn1 = Connection.objects.create(backend=self.backend, identity="254111111111")
        self.conn2 = Connection.objects.create(backend=self.backend, identity="254222222222")
        self.conn3 = Connection.objects.create(backend=self.backend, identity="254333333333")

    def login(self, user):
        self.assertTrue(self.client.login(username=user.username, password=user.username))

    def assertPost(self, url, post_data):
        response = self.client.post(url, post_data, follow=True)
        self.assertEquals(200, response.status_code, "Post got a non 200 response code.  Got %d instead." % response.status_code)
        self.assertTrue(not 'form' in response.context, "Post response had form within it.")
        return response

    def assertAtURL(self, response, url):
        self.assertEquals(response.request['PATH_INFO'], url,
                        "At url: %s instead of %s" % (response.request['PATH_INFO'], url))

    def assertRedirect(self, response, url):
        self.assertEquals(302, response.status_code)
        segments = urlparse(response.get('Location', None))
        self.assertEquals(segments.path, url)

    def assertInitial(self, response, field, value):
        self.assertTrue('form' in response.context)
        form = response.context['form']
        self.assertTrue(field in form.initial)
        self.assertEquals(value, form.initial[field])

    def assertSMSResponse(self, db_msg, text):
        from rapidsms_httprouter.models import Message
        responses = Message.objects.filter(in_response_to=db_msg)

        if not responses:
            self.fail("No response found for message: '%s'" % db_msg.text)

        for response in responses:
            if response.text.find(text) >= 0:
                return

        self.fail("Unable to find text '%s' in response '%s'" % (text, response.text))

    def sendSMS(self, msg, connection=None):
        if not connection:
            connection = self.conn1

        router = get_router()
        db_msg = router.handle_incoming(connection.backend.name, connection.identity, msg)        
        return db_msg
