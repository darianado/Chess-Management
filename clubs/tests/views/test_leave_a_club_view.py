"""Tests for the leave club view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club


class LeaveClubTest(TestCase):
    """Tests for the leave club view."""
    fixtures = ['clubs/tests/fixtures/default_user_john.json',
                'clubs/tests/fixtures/default_club_hame.json',
                'clubs/tests/fixtures/default_membership_john_hame.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.user = User.objects.get(email="johndoe@example.org")
        self.member = Membership.objects.get(club = self.club, user = self.user)
        self.url = reverse('leave_a_club', kwargs={'club_id': self.club.id})

    def test_leave_a_club_url(self):
        self.assertEqual(self.url,f'/leave_a_club/{self.club.id}')

    def test_leave_when_not_logged_in(self):
        user_count_before = Club.objects.count()
        redirect_url = reverse('log_in')
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        user_count_after = Club.objects.count()
        self.assertEqual(user_count_after, user_count_before)
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)

    def test_leave_when_an_owner(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        membership = Membership.objects.get(user=self.user, club=self.club)
        membership.role = 1
        membership.save()
        member_count_before = Membership.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before)
        response_url = reverse('show_club', kwargs={"club_id": self.club.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
        )
        self.assertTemplateUsed(response, 'show_club.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_successful_leave_a_club(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        member_count_before = Membership.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before-1)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_leave_a_club(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        member_count_before = Membership.objects.count()
        response = self.client.post(self.url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
