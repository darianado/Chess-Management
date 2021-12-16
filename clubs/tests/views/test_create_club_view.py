from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User, Membership, Events

class NewPostTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_user_jane.json'

    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='johndoe@example.org')
        self.url = reverse('create_club')
        self.data = { 'club_name': 'Hame Chess Club', 'location':"SE1 4XA", 'description':'We love chess'}

    def test_create_club_url(self):
        self.assertEqual(self.url,'/create_club/')

    def test_create_club_redirects_when_not_logged_in(self):
        user_count_before = Club.objects.count()
        redirect_url = reverse('log_in')
        response = self.client.post(self.url, self.data, follow=True)
        self.assertRedirects(response, redirect_url,
            status_code=302, target_status_code=200, fetch_redirect_response=True
        )
        user_count_after = Club.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)

    def test_successful_create_club(self):
        self.client.login(email=self.user.email, password="Password123")
        club_count_before = Club.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_after, club_count_before+1)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_create_club_with_blank_club_name(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        club_count_before = Club.objects.count()
        self.data['club_name'] = ""
        response = self.client.post(self.url, self.data, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_after, club_count_before)
        self.assertTemplateUsed(response, 'create_club.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_create_club_with_blank_location(self):
        self.client.login(email='johndoe@example.org', password='Password123')
        club_count_before = Club.objects.count()
        self.data['location'] = ""
        response = self.client.post(self.url, self.data, follow=True)
        club_count_after = Club.objects.count()
        self.assertEqual(club_count_after, club_count_before)
        self.assertTemplateUsed(response, 'create_club.html')

    def test_successful_get_to_create_club_page(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, self.data, follow=True)
        self.assertTemplateUsed(response, 'create_club.html')

    def test_successful_create_club_owner_for_club(self):
        self.client.login(email=self.user.email, password="Password123")
        member_count_before = Membership.objects.count()
        response = self.client.post(self.url, self.data, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before+1)
        new_club = Club.objects.get(club_name=self.data.get("club_name"))
        new_member = Membership.objects.get(club=new_club)
        self.assertEqual(self.user, new_member.user)
        self.assertEqual(new_member.role, 1)
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)
