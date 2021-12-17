"""Tests for the apply club view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club


class ClubApplyTest(TestCase):
    """Tests for the apply club view."""
    fixtures = ['clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club_hamersmith.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hamersmith Chess Club")
        self.userMark = User.objects.get(email="markvue@example.org")
        self.url = reverse('apply_to_club', kwargs={'club_id': self.club.id})

    def test_apply_to_club_url(self):
        self.assertEqual(self.url,f'/apply/{self.club.id}')

    def test_apply_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_apply_with_invalid_club_id(self):
        self.client.login(email=self.userMark.email, password="Password123")
        url = reverse('apply_to_club', kwargs={'club_id': 999999})
        member_count_before = Membership.objects.count()
        response = self.client.get(url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_apply_when_already_at_least_applicant(self):
        self.client.login(email=self.userMark.email, password="Password123")
        Membership.objects.create(
            user=self.userMark,
            club=self.club,
            role=1
        )
        member_count_before = Membership.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before)
        redirect_url = reverse("show_club", kwargs={"club_id": self.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


    def test_successful_apply_to_club(self):
        self.client.login(email=self.userMark.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMark.email, password="Password123"))
        member_count_before = Membership.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Membership.objects.count()
        self.assertEqual(member_count_after, member_count_before+1)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_apply_to_club(self):
        self.client.login(email=self.userMark.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMark.email, password="Password123"))
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
