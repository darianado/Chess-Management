
from django.test import TestCase
from django.urls import reverse
from clubs.models import Membership, Participant, Match, User, Tournament, Club
from clubs import views

class GetWinnerTestCase(TestCase):
     
    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",

        "clubs/tests/fixtures/default_club_hame.json",

        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",

        "clubs/tests/fixtures/default_tournament_hame.json",

        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_participant_jane.json",

        "clubs/tests/fixtures/default_match_john_jane.json",

    ]

    def setUp(self):
        self.tournament = Tournament.objects.get(name= "Yetti")
        self.match = Match.objects.get(id=1)
        self.match.match_status=3
        self.match.match_round=1
        self.match.save()
        self.looserJane = Participant.objects.get(id=2)
        self.looserJane.is_active=False
        self.looserJane.save()
        

        self.userMiki = User.objects.get(email="mikidoe@example.org")

        self.url = reverse("matches", kwargs={'tournament_id': self.tournament.id})

    def test_right_winner(self):
        self.client.login(email=self.userMiki.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Winner is John")

    def test_no_winner_yet(self):
        self.looserJane.is_active=True
        self.looserJane.save()
        self.client.login(email=self.userMiki.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Winner is")

