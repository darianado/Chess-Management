"""Test suite for event list view."""
from django.test import TestCase
from clubs.models import Events, User
from django.urls import reverse

class EventsListViewTestCase(TestCase):
    """Test suite for the event list view."""

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_club_hame.json',
        'clubs/tests/fixtures/default_action_john.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email="johndoe@example.org")
        self.url = reverse('events_list')

    def test_events_list_url(self):
        self.assertEqual(self.url,f'/events/')

    def test_get_events(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "Promoted")
        self.assertContains(response, "Hame Chess Club")

    def test_get_events_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_events_with_no_events(self):
        self.client.login(email=self.user.email, password="Password123")
        Events.objects.filter(user=self.user).delete()
        response = self.client.get(self.url)
        self.assertNotContains(response, "Promoted")
        self.assertNotContains(response, "Hame Chess Club")
