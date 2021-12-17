"""Unit tests of the create tournament form."""
from django import forms
from django.urls import reverse
from django.test import TestCase
from clubs.forms import CreateTournamentForm
from clubs.models import User, Club, Membership, Tournament
from django.db.models import Q

class CreateTournamentFormTestCase(TestCase):
    """Unit tests of the create tournament form."""

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_club_hame.json',
        'clubs/tests/fixtures/default_membership_john_hame.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/other_memberships.json',
        'clubs/tests/fixtures/default_tournament_hame.json',
    ]

    def setUp(self):
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.memberJohn = Membership.objects.get(user=self.userJohn, club=self.clubHame)
        self.userMiki = User.objects.get(email='mikidoe@example.org') #coorganiser 
        self.memberMiki = Membership.objects.get(user=self.userMiki, club=self.clubHame)
        self.url = reverse('tournament', kwargs={'club_id': self.clubHame.id})

        self.possible_coorganisers = Membership.objects.filter(Q(club=self.clubHame) & (Q(role=2) | Q(role=1) )).exclude(user=self.userJohn)

        self.form_input = {
            'name': 'Mikii',
            'description': 'The first ever tournament for club hame',
            #  'deadline': '2022-12-10T21:44:21.082Z',
            'deadline': '4/12/2022',
            'coorganisers': ['5'],
            "capacity": 16, 
        }

    def test_create_tournament_url(self):
        self.assertEqual(self.url,f'/create_tournament/{self.clubHame.id}')

    def test_form_has_necessary_fields(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        form = CreateTournamentForm(initial={"coorganisers":self.possible_coorganisers})
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('deadline', form.fields)
        self.assertIn('coorganisers', form.fields)
        self.assertIn('capacity', form.fields)


    def test_valid_create_tournament_form(self):
        form = CreateTournamentForm(initial={"coorganisers":self.possible_coorganisers}, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_correct_minimal_capacity(self):
        self.form_input["capacity"] = 2
        form = CreateTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_correct_max_capacity(self):
        self.form_input["capacity"] = 16
        form = CreateTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_incorrect_max_capacity(self):
        self.form_input["capacity"] = 20
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_incorrect_min_capacity(self):
        self.form_input["capacity"] = -1
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_correct_deadline(self):
        self.form_input['deadline'] = "12/12/2022"
        form = CreateTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_incorrect_deadline(self):
        self.form_input['deadline'] = "123/123/2022"
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_incorrect_deadline(self):
        self.form_input['deadline'] = "4/5/1925"
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_shows_correct_coorganisers(self):
        self.form_input['coorganisers'] = ['5']
        form = CreateTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_shows_doesn_show_organiser_in_coorganisers(self):
        self.form_input['coorganisers'] = ['5']
        form = CreateTournamentForm(data=self.form_input)
        self.assertTrue(form.is_valid())

   
