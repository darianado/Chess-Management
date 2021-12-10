from django.test import TestCase
from django.core.exceptions import ValidationError

from clubs.models import Participant, Tournament

class ParticipantModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_participant_jane.json"
    ]

    def setUp(self):
        self.participantJohn = Participant.objects.get(id=1)
        self.participantJane = Participant.objects.get(id=2)

    def test_tournament_cannot_be_empty(self):
        self.participantJohn.tournament = None
        self._assert_participant_is_invalid()

    def test_member_cannot_be_empty(self):
        self.participantJohn.member = None
        self._assert_participant_is_invalid()

    def test_score_cannot_be_empty(self):
        self.participantJohn.score = None
        self._assert_participant_is_invalid()

    def test_is_active_cannot_be_empty(self):
        self.participantJohn.is_active = None
        self._assert_participant_is_invalid()



    def test_organiser_cannot_be_a_participant(self):
        self.participantJohn = Tournament.objects.get(id=1).organiser
        self._assert_participant_is_invalid()



    def test_score_need_not_be_unique(self):
        self.participantJohn.score = self.participantJane.score
        self._assert_participant_is_valid()

    def test_is_active_need_not_be_unique(self):
        self.participantJohn.is_active = self.participantJane.is_active
        self._assert_participant_is_valid()



    def test_score_can_be_0(self):
        self.participantJohn.score = 0
        self._assert_participant_is_valid()

    def test_score_cannot_be_less_than_0(self):
        self.participantJohn.score = -1
        self._assert_participant_is_invalid()


    def _assert_participant_is_valid(self):
        try:
            self.participantJohn.full_clean()
        except (ValidationError):
            self.fail('Test participant should be valid')

    def _assert_participant_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.participantJohn.full_clean()
