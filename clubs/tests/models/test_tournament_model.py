from django.test import TestCase
from django.core.exceptions import ValidationError

from clubs.models import Tournament

class TournamentModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hamersmith.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_tournament_hamersmith.json"
    ]

    def setUp(self):
        self.tournamentYetti = Tournament.objects.get(name="Yetti")
        self.tournamentAlaska = Tournament.objects.get(name="Alaska")

    def test_name_cannot_be_empty(self):
        self.tournamentYetti.name = None
        self._assert_tournament_is_invalid()

    def test_name_may_contain_50_characters(self):
        self.tournamentYetti.name = "a" * 50
        self._assert_tournament_is_valid()

    def test_name_cannot_contain_51_characters(self):
        self.tournamentYetti.name = "a" * 51
        self._assert_tournament_is_invalid()

    def test_deadline_cannot_be_empty(self):
        self.tournamentYetti.deadline = None
        self._assert_tournament_is_invalid()

    def test_organiser_cannot_be_empty(self):
        self.tournamentYetti.organiser = None
        self._assert_tournament_is_invalid()

    def test_coorganisers_can_be_empty(self):
        self.tournamentYetti.coorganiser = None
        self._assert_tournament_is_valid()

    def test_club_cannot_be_empty(self):
        self.tournamentYetti.club = None
        self._assert_tournament_is_invalid()

    def test_capacity_cannot_be_empty(self):
        self.tournamentYetti.capacity = None
        self._assert_tournament_is_invalid()

    def test_description_can_be_empty(self):
        self.tournamentYetti.description = None
        self._assert_tournament_is_valid()

    def test_description_may_contain_260_characters(self):
        self.tournamentYetti.description = "a" * 260
        self._assert_tournament_is_valid()

    def test_description_cannot_contain_261_characters(self):
        self.tournamentYetti.description = "a" * 261
        self._assert_tournament_is_invalid()



    def test_name_must_be_unique(self):
        self.tournamentYetti.name = self.tournamentAlaska.name
        self._assert_tournament_is_invalid()

    def test_description_need_not_be_unique(self):
        self.tournamentYetti.description = self.tournamentAlaska.description
        self._assert_tournament_is_valid()

    def test_deadline_need_not_be_unique(self):
        self.tournamentYetti.deadline = self.tournamentAlaska.deadline
        self._assert_tournament_is_valid()

    def test_organiser_need_not_be_unique(self):
        self.tournamentYetti.organiser = self.tournamentAlaska.organiser
        self._assert_tournament_is_valid()

    def test_coorganisers_need_not_be_unique(self):
        self.tournamentYetti.coorganisers.set(self.tournamentAlaska.coorganisers.all())
        self._assert_tournament_is_valid()

    def test_club_need_not_be_unique(self):
        self.tournamentYetti.club = self.tournamentAlaska.club
        self._assert_tournament_is_valid()

    def test_capacity_need_not_be_unique(self):
        self.tournamentYetti.capacity = self.tournamentAlaska.capacity
        self._assert_tournament_is_valid()



    def test_capacity_can_be_2(self):
        self.tournamentYetti.capacity = 2
        self._assert_tournament_is_valid()

    def test_capacity_can_be_96(self):
        self.tournamentYetti.capacity = 96
        self._assert_tournament_is_valid()

    def test_capacity_cannot_be_1(self):
        self.tournamentYetti.capacity = 1
        self._assert_tournament_is_invalid()

    def test_capacity_cannot_be_97(self):
        self.tournamentYetti.capacity = 97
        self._assert_tournament_is_invalid()

    

    def _assert_tournament_is_valid(self):
        try:
            self.tournamentYetti.full_clean()
        except (ValidationError):
            self.fail('Test tournament should be valid')

    def _assert_tournament_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tournamentYetti.full_clean()
