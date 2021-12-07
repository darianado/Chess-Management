from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Members, Club


class ResendApplicationTest(TestCase):
    fixtures = ['clubs/tests/fixtures/default_user_mark.json',
                'clubs/tests/fixtures/default_club_hame.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.user = User.objects.get(email="Markvue@example.org")
        self.url = reverse('resend_application', kwargs={'club_id': self.club.id})

    def test_resend_application_url(self):
        self.assertEqual(self.url,f'/resend_application/{self.club.id}')

    def test_successful_resend_application(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        response = self.client.get(self.url, follow=True)
        response_url = reverse('resend_application', kwargs={'club_id': self.club.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resend_application.html')
