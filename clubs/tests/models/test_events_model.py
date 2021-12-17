"""Unit tests for the Events model."""
from django.test import TestCase
from clubs.models import Club, Membership, User, Events
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

class EventsModelTest(TestCase):
    """Unit tests for the Events model."""

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

# tests for action  

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

    def test_action_string_is_accepted_and_colour_is_green_when_action_is_1(self):
        self.event.action = 1
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Accepted")
        self.assertEqual(colour, "green")

    def test_action_string_is_applied_and_colour_is_yellow_when_action_is_2(self):
        self.event.action = 2
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Applied")
        self.assertEqual(colour, "yellow")

    def test_action_string_is_rejected_and_colour_is_red_when_action_is_3(self):
        self.event.action = 3
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Rejected")
        self.assertEqual(colour, "red")

    def test_action_string_is_promoted_and_colour_is_green_when_action_is_4(self):
        self.event.action = 4
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Promoted")
        self.assertEqual(colour, "green")

    def test_action_string_is_demoted_and_colour_is_red_when_action_is_5(self):
        self.event.action = 5
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Demoted")
        self.assertEqual(colour, "red")

    def test_action_string_is_kicked_and_colour_is_red_when_action_is_6(self):
        self.event.action = 6
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, "Kicked")
        self.assertEqual(colour, "red")

    def test_action_string_is_none_and_colour_is_none_when_action_is_7(self):
        self.event.action = 7
        string = self.event.getActionString()
        colour = self.event.getActionColour()
        self.assertEqual(string, None)
        self.assertEqual(colour, None)
