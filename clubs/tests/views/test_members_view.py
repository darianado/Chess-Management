from django.test import TestCase
from django.urls import reverse

from clubs.models import Club, Members, User

class ShowMemberListTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_member_john_hame.json",
        "clubs/tests/fixtures/default_member_john_hamersmith.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.clubHamersmith = Club.objects.get(club_name="Hamersmith Chess Club")

        self.urlHame = reverse('show_members', kwargs={'club_id': self.clubHame.id})
        self.urlHamersmith = reverse('show_members', kwargs={'club_id': self.clubHamersmith.id})

    def test_show_club_members_url(self):
        self.assertEqual(self.urlHame, f'/club/{self.clubHame.id}/members/')
        self.assertEqual(self.urlHamersmith, f'/club/{self.clubHamersmith.id}/members/')

    def test_get_club_Hame_members(self):
        response = self.client.get(self.urlHame)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "partials/members_list_table.html")
        self.assertContains(response, self.userJohn.get_full_name())
        self.assertNotContains(response, self.userJane.get_full_name())
