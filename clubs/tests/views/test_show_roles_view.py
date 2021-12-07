from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.helpers import  Role
from clubs.models import Club, User, Membership

class ShowrolesTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",

        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",

        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json"
    ]

    def setUp(self):
        self.userJane = User.objects.get(email='janedoe@example.org') #owner
        self.userJohn = User.objects.get(email="johndoe@example.org") #member
        self.userMiki = User.objects.get(email='mikidoe@example.org') #officer
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        

        self.urlHameApplic = reverse('show_roles', kwargs={'club_id': self.clubHame.id})

    def test_show_roles_url(self):
        self.assertEqual(self.urlHameApplic,f'/club/{self.clubHame.id}/roles')

    def test_get_show_club_roles_when_not_logged_in(self):
        response = self.client.get(self.urlHameApplic)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_get_show_club_roles_when_not_a_owner_of_the_club(self):
        self.client.login(email=self.userMiki.email, password="Password123")
        response = self.client.get(self.urlHameApplic)
        redirect_url = reverse("club_list")
        self.assertRedirects(response, redirect_url, status_code=302,target_status_code=200)


    def test_get_show_club_roles_when_owner_of_the_club(self):
        self.client.login(email=self.userJane.email, password="Password123")
        response = self.client.get(self.urlHameApplic)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, "partials/roles_list_table.html")
        self.assertContains(response, self.userJohn.get_full_name())
        self.assertContains(response, self.userMiki.get_full_name())

    def test_get_show_roles_with_invalid_id(self):
        self.client.login(email=self.userJane.email, password="Password123")
        url = reverse('show_roles', kwargs={'club_id': self.clubHame.id+9999999})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')
