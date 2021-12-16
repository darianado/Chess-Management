from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.models import Club, User, Membership, Tournament, Participant, Match
from clubs import views

class HaveDrawnTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_participant_jane.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_match_john_charlie.json",
        "clubs/tests/fixtures/default_match_john_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/other_participants.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
    ]

    def setUp(self):
        self.tournament = Tournament.objects.get(name = 'Yetti')
        self.match_John_Charlie = Match.objects.get(id=1)
        self.match_John_Charlie.match_status=2
        self.match_John_Charlie.match_round=1
        self.match_John_Charlie.save()
        self.match_John_Jane = Match.objects.get(id=2)
        self.match_John_Jane.match_status=3
        self.match_John_Jane.match_round=2
        self.match_John_Jane.save()
        self.userMiki = User.objects.get(email="mikidoe@example.org")


    def test_haveDrawn(self):
        haveDrawn = views.haveDrawn(tournament = self.tournament, matches = None, match_round = self.match_John_Charlie.match_round)
        self.assertEqual(haveDrawn, True)

    def test_not_haveDrawn(self):
        haveDrawn = views.haveDrawn(tournament = self.tournament, matches = None, match_round = self.match_John_Jane.match_round)
        self.assertEqual(haveDrawn, False)
