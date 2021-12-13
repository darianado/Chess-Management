from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club


class ResendApplicationTest(TestCase):
    fixtures = ['clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/default_club_hame.json',
                'clubs/tests/fixtures/other_memberships.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hame Chess Club")
        self.user = User.objects.get(email="markvue@example.org")
        self.userViktor = User.objects.get(email="victordoe@example.org")
        self.member = Membership.objects.get(club=self.club,user=self.user)
        self.url = reverse('resend_application', kwargs={'club_id': self.club.id})

    def test_resend_application_url(self):
        self.assertEqual(self.url,f'/resend_application/{self.club.id}')

    def test_successful_resend_application(self):
        self.client.login(email=self.user.email, password="Password123")
        self.assertTrue(self.client.login(email=self.user.email, password="Password123"))
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resend_application.html')

    def test_unsuccessful_resend_application(self):
        self.client.login(email=self.userViktor.email, password="Password123")
        url = reverse('resend_application', kwargs={'club_id': self.club.id+9999999})
        response = self.client.get(url, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'partials/dashboard.html')
        
    def test_unsuccessful_resend_application_when_user_not_applicant(self):
        self.client.login(email=self.userViktor.email, password="Password123")
        url = reverse('resend_application', kwargs={'club_id': self.club.id})
        response = self.client.get(url, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'partials/dashboard.html')
        


        
