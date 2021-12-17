"""Unit tests of the create club form."""
from django.test import TestCase
from clubs.forms import CreateClubForm
from clubs.models import User, Club
from django.urls import reverse


class CreateClubFormTestCase(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hame.json"
    ]

    """Unit tests of the create club form."""
    def setUp(self):
        self.form_input = {
            'club_name': 'Kings',
            'location': 'EC1N 8TE',
            'description': 'This is a chess club for Kings students',
        }
        self.user = User.objects.get(email='johndoe@example.org')
        self.club = Club.objects.get(club_name='Hame Chess Club')

    def test_form_contains_required_fields(self):
        form = CreateClubForm()
        self.assertIn("club_name", form.fields)
        self.assertIn("location", form.fields)
        self.assertIn("description", form.fields)

    def test_form_accepts_valid_input(self):
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_club_name(self):
        self.form_input["club_name"] = ""
        form = CreateClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_location(self):
        self.form_input["location"] = ""
        form = CreateClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input["description"] = ""
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_club_name_must_be_unique(self):
        self.form_input["club_name"] = "Hame Chess Club"
        form = CreateClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_location_can_be_same(self):
        self.form_input["location"] = "SE1 4XA"
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_description_can_be_same(self):
        self.form_input["description"] = "We love chess"
        form = CreateClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())
