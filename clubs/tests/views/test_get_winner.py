from django.test import TestCase
from django.urls import reverse
from clubs.models import Participant, User, Tournament
from clubs import views

class GetWinnerTestCase(TestCase):
     
    fixtures = [
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/other_participants.json",
    ]

    # def setUp(self):
    #     self.tournament = Tournament.objects.get(name= "Yetti")
    #     for x in Participant.objects.all():
    #         x.is_active = False
    #     self.winner = Participant.objects.get(tournament= 1, member= 10)
    #     self.winner.is_active = True
    #     self.userMiki = User.objects.get(email='mikidoe@example.org')
    #     self.url = reverse("matches", kwargs={'tournament_id': self.tournament.id})

    # def test_only_one_active_participant(self):
    #     self.client.login(email=self.userMiki.email, password="Password123")
    #     response = self.client.get(self.url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(self.url, "Tracy")
