from django.test import TestCase
from django.core.exceptions import ValidationError

from clubs.models import Participant

class ParticipantModelTest(TestCase):

    fixtures = []

    def setUp(self):
        self.participantJohn = None
        self.participantJane = None

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
