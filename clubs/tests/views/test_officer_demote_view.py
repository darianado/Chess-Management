from django.test import TestCase
from django.urls import reverse
from clubs.helpers import  Role
from clubs.models import Club, User, Membership

class OfficerDemoteTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_club_hame.json",
    ]

    def setUp(self):
        self.userGreta = User.objects.get(email='greatdoe@example.org') #officer
        self.user = User.objects.get(email='janedoe@example.org') #Owner
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.member = Membership.objects.get(user=self.userGreta, club=self.club)

        self.url = reverse('officer_demote', kwargs={'member_id': self.member.id})



    def test_officer_demote_url(self):
        self.assertEqual(self.url,f'/officer_demote/{self.member.id}')

    def test_officer_demote_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_officer_demote_when_logged_in_but_invalid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('officer_demote', kwargs={'member_id': self.member.id+9999})
        response = self.client.post(url)
        redirect_url = reverse("club_list")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_officer_demote_when_logged_in_with_valid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertEqual(Membership.get_member_role(self.userGreta, self.club), Role.OFFICER)
        response = self.client.get(self.url)
        redirect_url = reverse("show_club", kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Membership.get_member_role(self.userGreta, self.club), Role.MEMBER)
