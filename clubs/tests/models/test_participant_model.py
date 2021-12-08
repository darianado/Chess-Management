from django.test import TestCase
from django.core.exceptions import ValidationError

class ParticipantModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def _assert_participant_is_valid(self):
        try:
            self.participant.full_clean()
        except (ValidationError):
            self.fail('Test participant should be valid')

    def _assert_participant_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.participant.full_clean()
