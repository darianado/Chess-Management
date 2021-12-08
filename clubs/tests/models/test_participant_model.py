from django.test import TestCase
from django.core.exceptions import ValidationError

class ParticipantModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def test_tournament_cannot_be_empty(self):
        pass

    def test_member_cannot_be_empty(self):
        pass

    def test_score_cannot_be_empty(self):
        pass

    def test_is_active_cannot_be_empty(self):
        pass



    def test_score_need_not_be_unique(self):
        pass

    def test_is_active_need_not_be_unique(self):
        pass



    def test_score_can_be_0(self):
        pass

    def test_score_cannot_be_less_than_0(self):
        pass


    def _assert_participant_is_valid(self):
        try:
            self.participant.full_clean()
        except (ValidationError):
            self.fail('Test participant should be valid')

    def _assert_participant_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.participant.full_clean()
