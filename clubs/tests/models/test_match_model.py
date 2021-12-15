from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from clubs.models import Match, Tournament

class MatchModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_participant_jane.json",
        "clubs/tests/fixtures/other_participants.json",
        "clubs/tests/fixtures/default_match_john_jane.json",
        "clubs/tests/fixtures/default_match_john_charlie.json"
    ]

    def setUp(self):
        self.matchOne = Match.objects.get(id=1)
        self.matchTwo = Match.objects.get(id=2)

    def test_tournament_cannot_be_empty(self):
        self.matchOne.tournament = None
        self._assert_match_is_invalid()

    def test_playerA_cannot_be_empty(self):
        self.matchOne.playerA = None
        self._assert_match_is_invalid()

    def test_playerB_cannot_be_empty(self):
        self.matchOne.playerB = None
        self._assert_match_is_invalid()

    def test_match_status_cannot_be_empty(self):
        self.matchOne.match_status = None
        self._assert_match_is_invalid()

    def test_match_round_cannot_be_empty(self):
        self.matchOne.match_round = None
        self._assert_match_is_invalid()


    def test_tournament_need_not_be_unique(self):
        self.matchOne.tournament = self.matchTwo.tournament
        self._assert_match_is_valid()

    def test_playerA_need_not_be_unique(self):
        self.matchOne.playerA = self.matchTwo.playerA
        self._assert_match_is_valid()

    def test_playerB_need_not_be_unique(self):
        self.matchOne.playerB = self.matchTwo.playerB
        self._assert_match_is_valid()

    def test_match_status_need_not_be_unique(self):
        self.matchOne.match_status = self.matchTwo.match_status
        self._assert_match_is_valid()

    def test_match_round_need_not_be_unique(self):
        self.matchOne.match_round = self.matchTwo.match_round
        self._assert_match_is_valid()



    def test_playerA_and_playerB_cannot_be_the_same(self):
        with self.assertRaises(IntegrityError):
            self.matchOne.playerA = self.matchOne.playerB
            self.matchOne.save()



    def test_match_status_can_be_1_2_3_4(self):
        self.matchOne.match_status = 1
        self._assert_match_is_valid()
        self.matchOne.match_status = 2
        self._assert_match_is_valid()
        self.matchOne.match_status = 3
        self._assert_match_is_valid()
        self.matchOne.match_status = 4
        self._assert_match_is_valid()

    def test_match_round_can_be_1_2_3_4(self):
        self.matchOne.match_round = 1
        self._assert_match_is_valid()
        self.matchOne.match_round = 2
        self._assert_match_is_valid()
        self.matchOne.match_round  = 3
        self._assert_match_is_valid()
        self.matchOne.match_round = 0
        self._assert_match_is_valid()

    def test_match_status_cannot_be_0(self):
        self.matchOne.match_status = 0
        self._assert_match_is_invalid()

    def test_match_round_can_be_0(self):
        self.matchOne.match_round = 0
        self._assert_match_is_valid()

    def test_match_round_cannot_be_5(self):
        self.matchOne.match_round = 5
        self._assert_match_is_invalid()

    def test_match_status_cannot_be_5(self):
        self.matchOne.match_status = 5
        self._assert_match_is_invalid()


    def _assert_match_is_valid(self):
        try:
            self.matchOne.full_clean()
        except (ValidationError):
            self.fail('Test match should be valid')

    def _assert_match_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.matchOne.full_clean()
