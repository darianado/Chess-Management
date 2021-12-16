from django.test import TestCase
from django.urls import reverse

from clubs.models import Club, Membership, User

class ShowMemberListTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.userGreta = User.objects.get(email="greatdoe@example.org")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")

        self.urlHame = reverse('show_members', kwargs={'club_id': self.clubHame.id})

    def test_show_club_members_url(self):
        self.assertEqual(self.urlHame, f'/club/{self.clubHame.id}/members/')

    def test_get_show_club_members_when_not_logged_in(self):
        response = self.client.get(self.urlHame)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_club_members_when_not_a_member_of_the_club(self):
        self.client.login(email=self.userJane.email, password="Password123")
        response = self.client.get(self.urlHame)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_club_Hame_members(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/members_list_table.html")
        self.assertContains(response, self.userJohn.get_full_name())
        self.assertNotContains(response, self.userJane.get_full_name())
        self.assertContains(response, self.userGreta.get_full_name())

    def test_get_club_Hame_members_when_logged_in_as_an_officer(self):
        self.client.login(email=self.userGreta.email, password="Password123")
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/members_list_table.html")
        self.assertContains(response, self.userJohn.get_full_name())
        self.assertNotContains(response, self.userJane.get_full_name())
        self.assertContains(response, self.userGreta.get_full_name())
