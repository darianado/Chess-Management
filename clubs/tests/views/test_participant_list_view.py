from django.test import TestCase
from django.urls import reverse

from clubs.models import Club, Membership, User, Tournament, Participant

class ParticipantListTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/other_participants.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.userCharlie = User.objects.get(email="charliedoe@example.org")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.memberJohn = Membership.objects.get(user=self.userJohn,club=self.clubHame)
        self.memberJohn.role = 2
        self.tournament = Tournament.objects.get(name="Yetti")

        self.url = reverse('participant_list', kwargs={'tournament_id': self.tournament.id})

    def test_participant_list_url(self):
        self.assertEqual(self.url, f'/participant/{self.tournament.id}')

    def test_get_participant_list_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_get_tournament_participant_officer(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/participant_list_table.html")
        self.assertContains(response, self.userCharlie.get_full_name())
        self.assertNotContains(response, self.userJane.get_full_name())

    def test_get_tournament_participant_clubowner(self):
        self.client.login(email=self.userJane.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/participant_list_table.html")
        self.assertContains(response, self.userCharlie.get_full_name())
        self.assertNotContains(response, self.userJane.get_full_name())
