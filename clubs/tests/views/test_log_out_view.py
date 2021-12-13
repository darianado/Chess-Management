"""Tests of the log out view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User
from clubs.tests.helper import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view."""

    fixtures = ['clubs/tests/fixtures/default_user_john.json']

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(email = 'johndoe@example.org')

    def test_log_out_url(self):
        self.assertEqual(self.url,'/log_out/')

    def test_get_log_out(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('welcome')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'welcome.html')
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
