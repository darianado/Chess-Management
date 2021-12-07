from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Members, Club


class ClubApplyTest(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user_mark.json',
                'clubs/tests/fixtures/default_club_hamersmith.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hamersmith Chess Club")
        self.userMark = User.objects.get(email="Markvue@example.org")
        self.url = reverse('apply_to_club', kwargs={'club_id': self.club.id})

    def test_apply_to_club_url(self):
        self.assertEqual(self.url,f'/apply/{self.club.id}')

    def test_successful_apply_to_club(self):
        self.client.login(email=self.userMark.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMark.email, password="Password123"))
        member_count_before = Members.objects.count()
        response = self.client.get(self.url, follow=True)
        member_count_after = Members.objects.count()
        self.assertEqual(member_count_after, member_count_before+1)
        response_url = reverse('club_list')
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'club_list.html')
