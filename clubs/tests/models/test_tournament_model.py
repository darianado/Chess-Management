from django.test import TestCase
from django.core.exceptions import ValidationError

class TournamentModelTest(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def test_name_cannot_be_empty(self):
        pass

    def test_name_may_contain_50_characters(self):
        pass

    def test_name_cannot_contain_51_characters(self):
        pass

    def test_deadline_cannot_be_empty(self):
        pass

    def test_organiser_cannot_be_empty(self):
        pass

    def test_coorganisers_cannot_be_empty(self):
        pass

    def test_club_cannot_be_empty(self):
        pass

    def test_capacity_cannot_be_empty(self):
        pass

    def test_description_can_be_empty(self):
        pass

    def test_description_may_contain_260_characters(self):
        pass

    def test_description_cannot_contain_261_characters(self):
        pass



    def test_name_must_be_unique(self):
        pass

    def test_description_need_not_be_unique(self):
        pass

    def test_deadline_need_not_be_unique(self):
        pass

    def test_organiser_need_not_be_unique(self):
        pass

    def test_coorganisers_need_not_be_unique(self):
        pass

    def test_club_need_not_be_unique(self):
        pass

    def test_capacity_need_not_be_unique(self):
        pass



    def test_capacity_can_be_2(self):
        pass

    def test_capacity_can_be_96(self):
        pass

    def test_capacity_cannot_be_1(self):
        pass

    def test_capacity_cannot_be_97(self):
        pass



    def _assert_tournament_is_valid(self):
        try:
            self.tournament.full_clean()
        except (ValidationError):
            self.fail('Test tournament should be valid')

    def _assert_tournament_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.tournament.full_clean()
