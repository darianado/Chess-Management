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
            'name': 'Yetti',
            'description': 'The first ever tournament for club hame',
            'deadline': '2022-12-10T21:44:21.082Z',
            'coorganisers': ['<Membership: Miki Doe Hame Chess Club>'],
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


    #  def test_valid_create_tournament_form(self):
         #  form = CreateTournamentForm(data=self.form_input)
        #  form = CreateTournamentForm(initial={"coorganisers":self.possible_coorganisers}, data=self.form_input)
        #  self.assertTrue(form.is_valid())
#
    #  def test_get_create_tournament_when_not_logged_in(self):
        #  response = self.client.get(self.url)
        #  redirect_url = reverse("log_in")
        #  self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
#
    #  def test_successful_redirect_after_succesful_create_tournament_form(self):
        #  self.client.login(email=self.userMiki.email, password="Password123")
        #  response = self.client.get(self.url)
        #  redirect_url = reverse("dashboard")
        #  self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        #  self.assertTemplateUsed(response,'create_tournament.html')
#
    #  def test_form_has_correct_minimal_capacity(self):
        #  self.form_input["capacity"] = "2"
        #  form = CreateTournamentForm(data=self.form_input)
        #  self.assertTrue(form.is_valid())
#
    #  def test_form_has_correct_max_capacity(self):
        #  self.form_input["capacity"] = "16"
        #  form = CreateTournamentForm(data=self.form_input)
        #  self.assertTrue(form.is_valid())
#
    def test_form_has_incorrect_max_capacity(self):
        self.form_input["capacity"] = "20"
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_has_incorrect_min_capacity(self):
        self.form_input["capacity"] = "-1"
        form = CreateTournamentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #  def test_form_has_correct_deadline(self):
        #  pass
    #  def test_form_has_incorrect_deadline(self):
        #  pass
    #  def test_form_shows_correct_coorganisers(self):
        #  pass
    #  def test_form_shows_doesn_show_organiser_in_coorganisers(self):
        #  pass
#
    #  def test_form_must_save_correctly(self):
        #  tournament = Tournament.objects.get(name='Yetti')
        #  form = CreateTournamentForm(instance=tournament, data=self.form_input)
        #  before_count = Tournament.objects.filter(club=self.clubHame).count()
        #  form.save()
        #  after_count = Tournament.objects.filter(club=self.clubHame).count()
        #  self.assertEqual(after_count, before_count+1)
        #  self.assertEqual(tournament.name,' Yetti')
        #  self.assertEqual(tournament.description, "The first ever tournament for club hame")
        #  self.assertEqual(tournament.deadline, '2021-12-07T21:44:21.082Z')
        #  self.assertEqual(tournament.coorganisers, [5])
        #  self.assertEqual(tournament.capacity, 16)
#
