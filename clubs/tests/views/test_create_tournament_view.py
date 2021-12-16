from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Membership, Events, Tournament

class CreateTournamentViewTestTestCase(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_user_jane.json',
        'clubs/tests/fixtures/default_club_hame.json',
        'clubs/tests/fixtures/other_users.json',
        'clubs/tests/fixtures/other_memberships.json',
        'clubs/tests/fixtures/default_membership_john_hame.json',
        'clubs/tests/fixtures/default_membership_jane_hame.json',

    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='greatdoe@example.org')
        self.userJohn = User.objects.get(email='johndoe@example.org')
        self.userJane = User.objects.get(email='janedoe@example.org')
        self.userCharlie = User.objects.get(email='charliedoe@example.org')
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.url = reverse('tournament', kwargs={'club_id': self.club.id})
        self.data = { 'name': 'Yetti', 'description':"The first ever tournament for club hame",
        'deadline':'2022-12-09T21:44:21.082Z', 'coorganisers': ['5'], 'capacity': 16}


    def test_create_tournament_url(self):
        self.assertEqual(self.url, f'/create_tournament/{self.club.id}')

    def test_create_tournament_redirects_when_not_logged_in(self):
        user_count_before = Tournament.objects.count()
        redirect_url = reverse('log_in')
        response = self.client.post(self.url, self.data, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = Tournament.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)

    def test_successful_create_tounament(self):
        self.client.login(email=self.user.email, password="Password123")
        tournament_count_before = Tournament.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        tournament_count_after = Tournament.objects.count()
        self.assertEqual(tournament_count_after, tournament_count_before+1)
        response_url = reverse('dashboard')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'home.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_create_tounament_with_blank_tounament_name(self):
        self.client.login(email=self.user.email, password='Password123')
        Tournament_count_before = Tournament.objects.count()
        self.data['name'] = ""
        response = self.client.post(self.url, self.data, follow=True)
        Tournament_count_after = Tournament.objects.count()
        self.assertEqual(Tournament_count_after, Tournament_count_before)
        self.assertTemplateUsed(response, 'create_tournament.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_create_tounament_with_blank_deadline(self):
        self.client.login(email=self.user.email, password='Password123')
        Tournament_count_before = Tournament.objects.count()
        self.data['deadline'] = ""
        response = self.client.post(self.url, self.data, follow=True)
        Tournament_count_after = Tournament.objects.count()
        self.assertEqual(Tournament_count_after, Tournament_count_before)
        self.assertTemplateUsed(response, 'create_tournament.html')

    def test_successful_get_to_create_tounament_page(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, self.data, follow=True)
        self.assertTemplateUsed(response, 'create_tournament.html')
