from django.test import TestCase
from django.urls import reverse
from clubs.helpers import reverse_with_next, Role
from clubs.models import Club, User, Members

class OfficerPromoteTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_member_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_members.json",
        "clubs/tests/fixtures/default_club_hame.json",
    ]

    def setUp(self):
        self.userMiki = User.objects.get(email='mikidoe@example.org') #officer
        self.user = User.objects.get(email='janedoe@example.org') #Owner
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.member = Members.objects.get(user=self.userMiki, club=self.club)

        self.url = reverse('officer_promote', kwargs={'member_id': self.member.id})



    def test_officer_promote_url(self):
        self.assertEqual(self.url,f'/officer_promote/{self.member.id}')

    def test_officer_promote_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_officer_promote_when_logged_in_but_invalid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('officer_demote', kwargs={'member_id': self.member.id+9999})
        response = self.client.post(url)
        redirect_url = reverse("club_list")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_officer_promote_when_logged_in_with_valid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertEqual(Members.get_member_role(self.userMiki, self.club), Role.OFFICER)
        response = self.client.get(self.url)
        redirect_url = reverse("show_club", kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Members.get_member_role(self.userMiki, self.club), Role.OWNER)
        self.assertEqual(Members.get_member_role(self.user, self.club), Role.OFFICER)

