from django.test import TestCase
from django.core.exceptions import ValidationError

class TournamentModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def _assert_tournament_is_valid(self):
        try:
            self.tournament.full_clean()
        except (ValidationError):
            self.fail('Test tournament should be valid')

    def _assert_tournament_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tournament.full_clean()
