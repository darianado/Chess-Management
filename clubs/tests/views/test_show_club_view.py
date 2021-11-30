from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, User

class ShowClubTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hamersmith.json"
    ]

    def setUp(self):
        self.club = Club.objects.get(club_name="Hamersmith Chess Club")
        self.url = reverse('show_club', kwargs={'club_id': self.club.id})
        self.userJohn = User.objects.get(email="johndoe@example.org")

    def test_show_club_url(self):
        self.assertEqual(self.url,f'/club/{self.club.id}')

    def test_get_show_club_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_club_with_valid_id(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_club.html')
        self.assertContains(response, "Hamersmith Chess Club")

    def test_get_show_club_with_invalid_id(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        url = reverse('show_club', kwargs={'club_id': self.club.id+1})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
        

        # tests for apply button and leave button

        #test for resend button

