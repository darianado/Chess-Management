"""Tests for the apply tournament view."""
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club, Tournament, Participant
from django.utils import timezone
from datetime import datetime, time, timedelta


class TournamentApplyTest(TestCase):
    """Tests for the apply tournament view."""
    fixtures = ['clubs/tests/fixtures/default_user_jane.json',
                'clubs/tests/fixtures/default_user_john.json',
                'clubs/tests/fixtures/default_membership_jane_hame.json',
                'clubs/tests/fixtures/default_membership_john_hame.json',
                'clubs/tests/fixtures/default_club_hame.json',
                'clubs/tests/fixtures/other_users.json',
                'clubs/tests/fixtures/other_memberships.json',
                'clubs/tests/fixtures/default_tournament_hame.json',
                'clubs/tests/fixtures/other_participants.json',
                'clubs/tests/fixtures/default_participant_john.json',
                'clubs/tests/fixtures/default_participant_jane.json',
    ]
    def setUp(self):
        super(TestCase, self).setUp()
        self.club = Club.objects.get(club_name="Hame Chess Club")

        self.tournament = Tournament.objects.get(name="Yetti")
        self.tournament.deadline = datetime.isoformat(datetime.now(tz=timezone.utc) + timedelta(days=1))
        self.tournament.save()

        self.userGreta = User.objects.get(email="greatdoe@example.org")
        self.userMary = User.objects.get(email="marydoe@example.org")
        self.userPrada = User.objects.get(email="pradadoe@example.org")

        self.member = Membership.objects.get(user=self.userPrada, club=self.club)
        self.participant = Participant.objects.get(member=self.member, tournament=self.tournament)

        self.url = reverse('apply_to_tournament', kwargs={'tournament_id': self.tournament.id})

    def test_apply_to_club_url(self):
        self.assertEqual(self.url,f'/apply_to_tournament/{self.tournament.id}')

    def test_unsuccessful_apply_to_tournament(self):
        self.client.login(email=self.userMary.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMary.email, password="Password123"))
        participant_count_before = Participant.objects.count()
        response = self.client.get(self.url, follow=True)
        participant_count_after = Participant.objects.count()
        self.assertEqual(participant_count_after, participant_count_before)
        response_url = reverse('show_tournament', kwargs={'tournament_id': self.tournament.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'show_tournament.html')

    def test_successful_apply_to_tournament(self):
        self.participant.delete()
        self.client.login(email=self.userMary.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMary.email, password="Password123"))
        participant_count_before = Participant.objects.count()
        response = self.client.get(self.url, follow=True)
        participant_count_after = Participant.objects.count()
        self.assertEqual(participant_count_after, participant_count_before + 1)
        response_url = reverse('show_tournament', kwargs={'tournament_id': self.tournament.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'show_tournament.html')

    def test_unsuccessful_apply_to_tournament_when_post(self):
        self.participant.delete()
        self.client.login(email=self.userMary.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMary.email, password="Password123"))
        participant_count_before = Participant.objects.count()
        response = self.client.post(self.url, follow=True)
        participant_count_after = Participant.objects.count()
        self.assertEqual(participant_count_after, participant_count_before)
        response_url = reverse('show_tournament', kwargs={'tournament_id': self.tournament.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'show_tournament.html')

    def test_unsuccessful_apply_to_tournament_by_deadline(self):
        self.tournament.deadline=datetime.isoformat(datetime.now(tz=timezone.utc) - timedelta(days=1))
        self.tournament.save()
        self.participant.delete()
        self.client.login(email=self.userMary.email, password="Password123")
        self.assertTrue(self.client.login(email=self.userMary.email, password="Password123"))
        participant_count_before = Participant.objects.count()
        response = self.client.post(self.url, follow=True)
        participant_count_after = Participant.objects.count()
        self.assertEqual(participant_count_after, participant_count_before)
        response_url = reverse('show_tournament', kwargs={'tournament_id': self.tournament.id})
        self.assertRedirects(
            response, response_url,
            status_code=302, target_status_code=200,
            fetch_redirect_response=True
        )
        self.assertTemplateUsed(response, 'show_tournament.html')
