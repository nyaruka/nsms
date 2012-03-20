from django.test import TestCase
from ..tests import MaternityTest
from django.core.urlresolvers import reverse

class DashboardTest(TestCase):

    def test_dashboard(self):
        # get our dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertRedirect(response, reverse('users.user_login'))
        self.login(self.admin)

        response = self.client.get(reverse('dashboard'))
        context = response.context


