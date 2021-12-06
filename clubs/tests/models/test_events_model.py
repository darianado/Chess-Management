from django.test import TestCase
from clubs.models import Club, Members, User, Events
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class EventsModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hame.json"
    ]

    def setUp(self):
        self.user = User.objects.get(email="johndoe@example.org")
        self.club = Club.objects.get(club_name="Hame Chess Club")

        self.event = Events.objects.create(
            club=self.club,
            user=self.user,
            action=2
        )

    def test_valid_event(self):
        self._assert_event_is_valid()

    def test_club_cannot_be_empty(self):
        self.event.club = None
        self._assert_event_is_invalid()

    def test_user_cannot_be_empty(self):
        self.event.user = None
        self._assert_event_is_invalid()

    def test_action_cannot_be_empty(self):
        self.event.action = None
        self._assert_event_is_invalid()

    def test_action_can_be_1(self):
        self.event.action = 1
        self._assert_event_is_valid()

    def test_action_cannot_be_0(self):
        self.event.action = 0
        self._assert_event_is_invalid()

    def test_action_cannot_be_7(self):
        self.event.action = 7
        self._assert_event_is_invalid()

    def test_action_cannot_be_blank(self):
        self.event.action = ""
        self._assert_event_is_invalid()

    def _assert_event_is_valid(self):
        try:
            self.event.full_clean()
        except (ValidationError):
            self.fail('Test event should be valid')

    def _assert_event_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.event.full_clean()
