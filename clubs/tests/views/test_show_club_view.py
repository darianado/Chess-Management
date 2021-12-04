from django.test import TestCase
from django.urls import reverse
from clubs.helpers import reverse_with_next
from clubs.models import Club, User

class ShowClubTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_member_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_members.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email='janedoe@example.org') #owner
        self.userCharlie = User.objects.get(email='charliedoe@example.org') #owner
        self.userVictor = User.objects.get(email='victordoe@example.org') #owner
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")

        self.urlHame = reverse('show_club', kwargs={'club_id': self.clubHame.id})

    def test_show_club_url(self):
        self.assertEqual(self.urlHame,f'/club/{self.clubHame.id}')

    def test_get_show_club_when_not_logged_in(self):
        response = self.client.get(self.urlHame)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_club_with_valid_id(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.assertContains(response, "Hame Chess Club")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        url = reverse('show_club', kwargs={'club_id': self.clubHame.id+9999999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
        


    #  def test_content_displayed_corectly(self):
        #  url = reverse('show_club', kwargs={'club_id': clubHamersmith.id})
        #  response = self.client.get(url)


    def test_correct_owner_information_shown(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane')

    def test_incorrect_owner_information_shown(self):
        self.client.login(email=self.userCharlie.email, password="Password123")
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Charlie')

    def test_apply_for_applicant_when_logged_in_user_is_user(self):
        self.client.login(email=self.userVictor.email, password="Password123")
        response = self.client.get(self.urlHame)

    #  def test_redirect_when_applicant(self):
        #  redirect_url = reverse_with_next(self.urlHame,'resend_application')
        #  response = self.client.get(self.urlHame)
        #  self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

        


