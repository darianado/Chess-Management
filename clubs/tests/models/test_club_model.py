"""Unit tests for the Club model."""
from django.test import TestCase
from clubs.models import Club
from django.core.exceptions import ValidationError

class ClubModelTest(TestCase):
    """Unit tests for the Club model."""

    fixtures = [
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_club_hame.json"
    ]

    def setUp(self):
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")

    def _assert_club_is_valid(self):
        try:
            self.clubHamersmith.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.clubHamersmith.full_clean()

# tests for club_name

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_club_name_cannot_be_blank(self):
        self.clubHamersmith.club_name = ''
        self._assert_club_is_invalid()

    def test_club_name_can_be_50_characters_long(self):
        self.clubHamersmith.club_name = 'x' * 50
        self._assert_club_is_valid()

    def test_club_name_cannot_be_over_50_characters_long(self):
        self.clubHamersmith.club_name = 'x' * 51
        self._assert_club_is_invalid()

    def test_club_name_must_be_unique(self):
        self.clubHamersmith.club_name = self.clubHame.club_name
        self._assert_club_is_invalid()


# tests for location

    def test_location_cannot_be_blank(self):
        self.clubHamersmith.location = ''
        self._assert_club_is_invalid()

    def test_location_can_be_100_characters_long(self):
        self.clubHamersmith.location = 'x' * 100
        self._assert_club_is_valid()

    def test_location_cannot_be_over_100_characters_long(self):
        self.clubHamersmith.location = 'x' * 101
        self._assert_club_is_invalid()

    def test_location_need_not_be_unique(self):
        self.clubHamersmith.location = self.clubHame.location
        self._assert_club_is_valid()

# tests for description

    def test_description_can_be_blank(self):
        self.clubHamersmith.description = ''
        self._assert_club_is_valid()

    def test_description_can_be_260_characters_long(self):
        self.clubHamersmith.description = 'x' * 260
        self._assert_club_is_valid()

    def test_description_cannot_be_over_260_characters_long(self):
        self.clubHamersmith.description = 'x' * 261
        self._assert_club_is_invalid()

    def test_description_need_not_be_unique(self):
        self.clubHamersmith.description = self.clubHame.description
        self._assert_club_is_valid()
