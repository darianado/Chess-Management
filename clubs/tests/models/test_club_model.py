from django.test import TestCase
from clubs.models import Club
from django.core.exceptions import ValidationError



class ClubModelTest(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
                club_name = "Hamersmith Chess Club", 
                location = "SE1 4XA",
                description = "We love chess",
        )
    def _create_second_club(self):
        club = Club.objects.create(
                club_name = "Hame Chess Club", 
                location = "SE1 4XA",
                description = "We love chess",
        )
        return club



    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

# tests for club_name

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_club_name_cannot_be_blank(self):
        self.club.club_name = ''
        self._assert_club_is_invalid()

    def test_club_name_can_be_50_characters_long(self):
        self.club.club_name = 'x' * 50
        self._assert_club_is_valid()

    def test_club_name_cannot_be_over_50_characters_long(self):
        self.club.club_name = 'x' * 51
        self._assert_club_is_invalid()

    def test_club_name_must_be_unique(self):
        second_club = self._create_second_club()
        self.club.club_name = second_club.club_name
        self._assert_club_is_invalid()


# tests for location

    def test_location_cannot_be_blank(self):
        self.club.location = ''
        self._assert_club_is_invalid()

    def test_location_can_be_100_characters_long(self):
        self.club.location = 'x' * 100
        self._assert_club_is_valid()

    def test_location_cannot_be_over_100_characters_long(self):
        self.club.location = 'x' * 101
        self._assert_club_is_invalid()

    def test_location_need_not_be_unique(self):
        second_club = self._create_second_club()
        self.club.location = second_club.location
        self._assert_club_is_valid()

# tests for description

    def test_description_can_be_blank(self):
        self.club.description = ''
        self._assert_club_is_valid()

    def test_description_can_be_260_characters_long(self):
        self.club.description = 'x' * 260
        self._assert_club_is_valid()

    def test_description_cannot_be_over_260_characters_long(self):
        self.club.description = 'x' * 261
        self._assert_club_is_invalid()

    def test_description_need_not_be_unique(self):
        second_club = self._create_second_club()
        self.club.location = second_club.location
        self._assert_club_is_valid()
