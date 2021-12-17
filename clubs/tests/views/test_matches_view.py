from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.models import Club, User, Membership, Tournament, Participant, Match

class MachesTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_participant_jane.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_match_john_charlie.json",
        "clubs/tests/fixtures/default_match_john_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/other_participants.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
    ]

    def setUp(self):

        self.userCharlie = User.objects.get(email='charliedoe@example.org')
        self.userGreta = User.objects.get(email='greatdoe@example.org')
        self.userMiki = User.objects.get(email='mikidoe@example.org')
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.tournament = Tournament.objects.get(name = 'Yetti')
        self.memberCharlie = Membership.objects.get(user=self.userCharlie, club = self.clubHame)
        self.memberGreta = Membership.objects.get(user=self.userGreta, club = self.clubHame)
        self.memberMiki = Membership.objects.get(user=self.userMiki, club = self.clubHame)
        self.participantCharlie = Participant.objects.get(member=self.memberCharlie, tournament = self.tournament)
        self.url = reverse('matches', kwargs={'tournament_id': self.tournament.id})

    def test_tournament_list_url(self):
        self.assertEqual(self.url,f'/matches/{self.tournament.id}')

    def test_get_tournament_list_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_tournament_list_with_invalid_id(self):
        self.client.login(email=self.userGreta.email, password="Password123")
        url = reverse("matches", kwargs={"tournament_id": 99999})
        response = self.client.get(url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_matches_organiser(self):
        self.client.login(email=self.userGreta.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/matches.html')

    def test_matches_coorganiser(self):
        self.client.login(email=self.userMiki.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/matches.html')

    def test_matches_participant(self):
        self.client.login(email=self.userCharlie.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/matches.html')
