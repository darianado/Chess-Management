from django.test import TestCase
from django.urls import reverse
from clubs.models import Club, Membership, User
from clubs.tests.helper import reverse_with_next

class UserProfileViewTestCase(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.urlJohn = reverse("show_user", kwargs={"user_id": 1})
        self.urlIncorrect = reverse("show_user", kwargs={"user_id": 3})

    def test_show_user_url(self):
        self.assertEqual(self.urlJohn, "/user/1")
        self.assertEqual(self.urlIncorrect, "/user/3")

    def test_get_show_user_when_not_logged_in(self):
        response = self.client.get(self.urlJohn, follow=True)
        redirect_url = reverse_with_next("log_in", self.urlJohn)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_show_user_with_valid_id_but_not_own_profile(self):
        self.client.login(email=self.userJane.email, password="Password123")
        janeMembership = Membership.objects.get(club=Club.objects.get(club_name="Hame Chess Club"), user=self.userJane)
        janeMembership.role = 3
        janeMembership.save()
        response = self.client.get(self.urlJohn)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_profile"], self.userJohn)
        self.assertNotContains(response, 'nu mi place sa joc sah')
        self.assertNotContains(response, 'johndoe@example.org')
        self.assertNotContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")

    def test_get_show_users_own_profile(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(self.urlJohn)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_profile"], self.userJohn)
        self.assertContains(response, 'nu mi place sa joc sah')
        self.assertContains(response, 'johndoe@example.org')
        self.assertContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")

    def test_get_show_user_with_valid_id_but_not_own_profile_and_viewer_is_officer_or_owner_of_a_common_club(self):
        self.client.login(email=self.userJane.email, password="Password123")
        response = self.client.get(self.urlJohn)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_profile"], self.userJohn)
        self.assertContains(response, 'nu mi place sa joc sah')
        self.assertContains(response, 'johndoe@example.org')
        self.assertContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")

    def test_case_when_id_is_incorrect(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(self.urlIncorrect, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_show_url_with_no_id_redirects_to_own_profile(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        response = self.client.get(reverse("show_user"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user_profile"], self.userJohn)
        self.assertContains(response, 'nu mi place sa joc sah')
        self.assertContains(response, 'johndoe@example.org')
        self.assertContains(response, 'Chess experience level')
        self.assertTemplateUsed(response, "show_user.html")
