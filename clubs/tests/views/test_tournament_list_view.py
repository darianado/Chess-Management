from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Membership, Tournament

class TournamentListTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_membership_jane_hamersmith.json",
        "clubs/tests/fixtures/default_membership_john_hamersmith.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_tournament_hamersmith.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email='janedoe@example.org')
        self.userJohn = User.objects.get(email='johndoe@example.org')
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")
        self.member = Membership.objects.get(user=self.user, club = self.clubHamersmith)
        self.clubowner = Membership.objects.get(user=self.userJohn, club = self.clubHamersmith)
        self.clubowner.role = 1
        self.tournament = Tournament.objects.get(name = 'Alaska')
        self.url = reverse('tournament_list', kwargs={'club_id': self.clubHamersmith.id})

    def test_tournament_list_url(self):
        self.assertEqual(self.url,f'/club/{self.clubHamersmith.id}/tournament')

    def test_get_tournament_list_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse('log_in')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_tournament_list_officer(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/tournaments_list_table.html')
        self.assertContains(response, self.tournament.name)

    def test_get_tournament_list_member(self):
        self.client.login(email=self.user.email, password="Password123")
        self.member.role = 3
        self.member.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/tournaments_list_table.html')
        self.assertContains(response, self.tournament.name)

    def test_get_tournament_list_clubowner(self):
        self.client.login(email=self.user.email, password="Password123")
        response_url = reverse('tournament_list', kwargs={'club_id':self.clubHamersmith.id})
        response = self.client.get(response_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/tournaments_list_table.html')
        self.assertContains(response, self.tournament.name)
