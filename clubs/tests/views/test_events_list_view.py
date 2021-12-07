from django.test import TestCase
from clubs.models import User
from django.urls import reverse

class EventsListViewTestCase(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_user_jane.json',
    ]

    def setUp(self):
        pass
