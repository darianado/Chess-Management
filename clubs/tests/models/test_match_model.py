from django.test import TestCase
from django.core.exceptions import ValidationError

class MatchModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def test_tournament_cannot_be_empty(self):
        pass

    def test_playerA_cannot_be_empty(self):
        pass

    def test_playerB_cannot_be_empty(self):
        pass

    def test_match_status_cannot_be_empty(self):
        pass




    def test_playerA_and_playerB_cannot_be_the_same(self):
        pass



    def test_match_status_can_be_1_2_3_4(self):
        pass

    def test_match_status_cannot_be_0(self):
        pass

    def test_match_status_cannot_be_5(self):
        pass



    def _assert_match_is_valid(self):
        try:
            self.match.full_clean()
        except (ValidationError):
            self.fail('Test match should be valid')

    def _assert_match_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.match.full_clean()
