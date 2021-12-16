"""Tests of the update active participants view."""
from django.test import TestCase
from django.urls import reverse
from clubs.tests.helper import reverse_with_next
from clubs.models import Club, User, Membership, Tournament, Participant, Match
from clubs import views

class updateActiveParticipantsTest(TestCase):
    """Tests of the update active participants view."""
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
        self.match_John_Charlie.match_status=4
        self.match_John_Charlie.match_round=1
        self.match_John_Charlie.save()
        self.match_John_Jane = Match.objects.get(id=2)
        self.match_John_Jane.match_status=3
        self.match_John_Jane.match_round=2
        self.match_John_Jane.save()
        self.userMiki = User.objects.get(email="mikidoe@example.org")


    def test_update_active_participants_when_status_is_4(self):
        update = views.updateActiveParticipants(matches = [self.match_John_Charlie])
        self.assertEqual(self.match_John_Charlie.playerA.is_active, False)

    def test_update_active_participants_when_status_is_3(self):
        update = views.updateActiveParticipants(matches = [self.match_John_Jane])
        self.assertEqual(self.match_John_Jane.playerB.is_active, False)

    def test_update_active_participants_when_status_is_2(self):
        self.match_John_Jane.match_status=2
        self.match_John_Jane.match_round=2
        self.match_John_Jane.save()
        update = views.updateActiveParticipants(matches = [self.match_John_Jane])
        self.assertEqual(self.match_John_Jane.playerB.is_active, True)
