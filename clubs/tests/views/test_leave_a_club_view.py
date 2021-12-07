from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Members, Club


class LeaveClubTest(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user_john.json',
                'clubs/tests/fixtures/default_club_hame.json',
                'clubs/tests/fixtures/default_member_john_hame.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.user = User.objects.get(email="johndoe@example.org")
        self.member = Members.objects.get(club = self.club, user = self.user)
        self.url = reverse('leave_a_club', kwargs={'club_id': self.club.id})

    def test_leave_a_club_url(self):
        self.assertEqual(self.url,f'/leave_a_club/{self.club.id}')

    def test_successful_leave_a_club(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        member_count_before = Members.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Members.objects.count()
        self.assertEqual(member_count_after, member_count_before-1)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
