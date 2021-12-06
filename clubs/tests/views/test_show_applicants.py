from django.test import TestCase
from django.urls import reverse
from clubs.helpers import reverse_with_next
from clubs.models import Club, User

class ShowClubTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_member_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_members.json",

        "clubs/tests/fixtures/default_applicants_hame.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email='janedoe@example.org') #owner
        self.userCharlie = User.objects.get(email='charliedoe@example.org') #owner
        self.userVictor = User.objects.get(email='victordoe@example.org') #owner
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")

        self.urlHame = reverse('show_applicants', kwargs={'club_id': self.clubHame.id})

    def test_show_applicants_url(self):
        self.assertEqual(self.urlHame,f'/club/{self.clubHame.id}')

    def test_get_show_applicants_with_valid_id(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "partials/applicants_as_table.html")

    def test_get_show_applicants_with_invalid_id(self):
        url = reverse('show_club', kwargs={'club_id': self.clubHame.id+9999999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
        
    # def test_apply_for_applicant_when_logged_in_user_is_user(self):
    #     self.client.login(email=self.userVictor.email, password="Password123")
    #     response = self.client.get(self.urlHame)
