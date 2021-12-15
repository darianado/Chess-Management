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
        'clubs/tests/fixtures/default_tournament_hame.json',

    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='greatdoe@example.org')
        self.userJohn = User.objects.get(email='johndoe@example.org')
        self.userJane = User.objects.get(email='janedoe@example.org')
        self.userCharlie = User.objects.get(email='charliedoe@example.org')
        self.url = reverse('create_club')
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.url = reverse('tournament', kwargs={'club_id': self.club.id})


    def test_create_tournament_url(self):
        self.assertEqual(self.url, f'/tournament/{self.club.id}')

    def test_get_create_tournament_is_forbidden(self):
        self.client.login(email=self.user.email, password="Password123")
        user_count_before = Club.objects.count()
        response = self.client.get(self.url, follow=True)
        response_url = reverse('tournament', kwargs={'club_id':self.clubHame.id})
        user_count_after = Club.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Charlie Doe")

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
        self.assertEqual(len(messages_list), 1)

    def test_successful_create_tounament(self):
        self.client.login(email=self.user.email, password="Password123")
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_after, club_count_before+1)
        response_url = reverse('dashboard')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    # def test_unsuccessful_create_tounament_with_blank_tounament_name(self):
    #     self.client.login(email='johndoe@example.org', password='Password123')
    #     club_count_before = Club.objects.count()
    #     self.data['club_name'] = ""
    #     response = self.client.post(self.url, self.data, follow=True)
    #     club_count_after = Club.objects.count()
    #     self.assertEqual(club_count_after, club_count_before)
    #     self.assertTemplateUsed(response, 'create_club.html')
    #     messages_list = list(response.context["messages"])
    #     self.assertEqual(len(messages_list), 1)
    #
    # def test_unsuccessful_create_club_with_blank_location(self):
    #     self.client.login(email='johndoe@example.org', password='Password123')
    #     club_count_before = Club.objects.count()
    #     self.data['location'] = ""
    #     response = self.client.post(self.url, self.data, follow=True)
    #     club_count_after = Club.objects.count()
    #     self.assertEqual(club_count_after, club_count_before)
    #     self.assertTemplateUsed(response, 'create_club.html')
    #
    # def test_successful_create_club_owner_for_club(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     member_count_before = Membership.objects.count()
    #     response = self.client.post(self.url, self.data, follow=True)
    #     member_count_after = Membership.objects.count()
    #     self.assertEqual(member_count_after, member_count_before+1)
    #     new_club = Club.objects.get(club_name=self.data.get("club_name"))
    #     new_member = Membership.objects.get(club=new_club)
    #     self.assertEqual(self.user, new_member.user)
    #     self.assertEqual(new_member.role, 1)
    #     messages_list = list(response.context["messages"])
    #     self.assertEqual(len(messages_list), 1)
