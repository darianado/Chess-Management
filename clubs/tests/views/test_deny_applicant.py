from django.test import TestCase
from django.urls import reverse
from clubs.helpers import  Role
from clubs.models import Club, User, Membership

class denyApplicantTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_club_hame.json",
    ]

    def setUp(self):
        self.userMiki = User.objects.get(email='mikidoe@example.org') #applicant
        self.user = User.objects.get(email='janedoe@example.org') #Owner
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.member = Membership.objects.get(user=self.userMiki, club=self.club)
        self.member.role=4
        self.member.save()

        self.url = reverse('deny_applicant', kwargs={'member_id': self.member.id})

    def test_deny_applicant_url(self):
        self.assertEqual(self.url,f'/deny_applicant/{self.member.id}')

    def test_deny_applicant_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_deny_applicant_when_logged_in_but_invalid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        url = reverse('deny_applicant', kwargs={'member_id': self.member.id+9999})
        response = self.client.get(url)
        redirect_url = reverse("club_list")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_deny_applicant_when_logged_in_with_valid_member_id(self):
        self.client.login(email=self.user.email, password='Password123')
        self.assertEqual(Membership.get_member_role(self.userMiki, self.club), Role.APPLICANT)
        response = self.client.get(self.url)
        redirect_url = reverse("show_club", kwargs={'club_id': self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertEqual(Membership.get_member_role(self.userMiki, self.club), None)

