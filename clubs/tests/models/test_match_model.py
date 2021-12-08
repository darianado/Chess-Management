from django.test import TestCase
from django.core.exceptions import ValidationError

class MatchModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def _assert_match_is_valid(self):
        try:
            self.match.full_clean()
        except (ValidationError):
            self.fail('Test match should be valid')

    def _assert_match_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.match.full_clean()
