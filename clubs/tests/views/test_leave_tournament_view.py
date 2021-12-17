from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.helpers import  Role
from clubs.models import Club, User, Membership, Tournament, Participant

class LeaveTournamentTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_participants.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_club_hame.json",
    ]

    def setUp(self):
        self.userCharlie = User.objects.get(email='charliedoe@example.org')
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.member = Membership.objects.get(user=self.userCharlie, club=self.club)
        self.tournament = Tournament.objects.get(name='Yetti')

        self.url = reverse('leave_tournament', kwargs={'tournament_id': self.tournament.id})

    def test_leave_tournament_url(self):
        self.assertEqual(self.url,f'/leave_tournament/{self.tournament.id}')

    def test_leave_tournament_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_leave_tournament_with_invalid_id(self):
        self.client.login(email=self.userCharlie.email, password='Password123')
        before_count = self.tournament.participants.all().count()
        url = reverse("leave_tournament", kwargs={"tournament_id": 99999})
        response = self.client.post(url, follow=True)
        after_count = self.tournament.participants.all().count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_leave_tournament_when_not_a_participant(self):
        self.client.login(email=self.userCharlie.email, password='Password123')
        Participant.objects.get(member=self.member, tournament=self.tournament).delete()
        before_count = self.tournament.participants.all().count()
        response = self.client.post(self.url, follow=True)
        after_count = self.tournament.participants.all().count()
        self.assertEqual(after_count, before_count)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_leave_tournament_successful(self):
        self.client.login(email=self.userCharlie.email, password='Password123')
        before_count = self.tournament.participants.all().count()
        response = self.client.post(self.url, follow=True)
        after_count = self.tournament.participants.all().count()
        self.assertEqual(after_count, before_count-1)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
