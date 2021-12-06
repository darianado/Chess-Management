from django.test import TestCase
from django.urls import reverse
from clubs.helpers import reverse_with_next
from clubs.models import Club, User

class ShowRolesTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_member_john_hame.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_members.json",
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org') #member
        self.userMiki = User.objects.get(email='mikidoe@example.org') #officer
        self.userGreta = User.objects.get(email='greatdoe@example.org') #officer

        self.clubHame = Club.objects.get(club_name="Hame Chess Club")

        self.urlHame = reverse('show_roles', kwargs={'club_id': self.clubHame.id})

    def test_show_club_members_url(self):
        self.assertEqual(self.urlHame, f'/club/{self.clubHame.id}/roles')


    # def test_get_show_club_roles_when_not_logged_in(self):
    #     response = self.client.get(self.urlHame)
    #     redirect_url = reverse("log_in")
    #     self.assertRedirects(response, redirect_url, status_code=200, target_status_code=200)
    #
    # def test_get_show_club_roles_when_not_an_owner_or_officer_of_the_club(self):
    #     self.client.login(email=self.user.email, password="Password123")
    #     response = self.client.get(self.urlHame)
    #     redirect_url = reverse("dashboard")
    #     self.assertRedirects(response, redirect_url, status_code=200, target_status_code=200)
    #
    # def test_get_club_Hame_roles(self):
    #     self.client.login(email=self.userMiki.email, password="Password123")
    #     response = self.client.get(self.urlHame)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "partials/roles_list_table.html")
    #     self.assertContains(response, self.user.get_full_name())
    #     self.assertContains(response, self.userMiki.get_full_name())
    #     self.assertContains(response, self.userGreta.get_full_name())
