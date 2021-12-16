from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.helpers import  Role
from clubs.models import Club, User, Membership, Tournament, Participant

class ShowClubTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_participants.json",
        "clubs/tests/fixtures/other_memberships.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email='markvue@example.org')
        self.userJohn = User.objects.get(email='johndoe@example.org')
        self.userCharlie = User.objects.get(email='charliedoe@example.org')
        self.userVictor = User.objects.get(email='victordoe@example.org')
        self.userMiki = User.objects.get(email='mikidoe@example.org')
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.tournament = Tournament.objects.get(name='Yetti')
        self.participant = Participant.objects.get(id=3)

        self.url = reverse('show_tournament', kwargs={'tournament_id': self.tournament.id})

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/tournament/{self.tournament.id}')

    def test_get_show_tournament_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_tournament_with_valid_id(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_tournament.html')
        self.assertContains(response, "Yetti")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(email=self.user.email, password="Password123")
        url = reverse('show_tournament', kwargs={'tournament_id':  self.tournament.id+9999999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')


    def test_correct_organiser_information_shown(self):
        self.client.login(email=self.userMiki.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Greta')

    def test_incorrect_owner_information_shown(self):
        self.client.login(email=self.userCharlie.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Jane')
