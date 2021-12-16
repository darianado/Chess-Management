"""Tests of the table view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club
from django.db.models import Q


class TableTest(TestCase):
    """Tests of the table view."""
    fixtures = ['clubs/tests/fixtures/default_user_john.json',
                'clubs/tests/fixtures/default_club_hame.json',
                'clubs/tests/fixtures/default_club_hamersmith.json',
                'clubs/tests/fixtures/default_membership_john_hame.json',
                'clubs/tests/fixtures/default_membership_john_hamersmith.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.memberJohnHame = Membership.objects.get(club = self.clubHame, user = self.userJohn)
        self.memberJohnHamersmith = Membership.objects.get(club = self.clubHamersmith, user = self.userJohn)
        self.url = reverse('table',)

    def test_table_url(self):
        self.assertEqual(self.url,f'/table/')

    def test_table_when_not_logged_in(self):
        response = self.client.post(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_view_correct_my_clubs_table(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userJohn.email, password="Password123"))
        john_clubs = [member.club for member in Membership.objects.filter(Q(user=self.userJohn) )]
        self.assertEqual(len(john_clubs), 2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'table.html')


    def test_incorrect_my_clubs_table(self):
        self.client.login(email=self.userJohn.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userJohn.email, password="Password123"))
        john_clubs = [member.club for member in Membership.objects.filter(Q(user=self.userJohn) )]
        self.assertNotEqual(len(john_clubs), 3)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'table.html')
