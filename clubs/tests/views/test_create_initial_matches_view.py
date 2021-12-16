from django.test import TestCase
from clubs.models import Match, Membership, Participant, Tournament
from clubs.tests.helper import reverse
from clubs.views import show_tournament

class CreateInitialMatchesViewTestCase(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/default_participant_jane.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
    ]

    def setUp(self):
        self.tournament = Tournament.objects.get(id=1)
        self.organiser = self.tournament.organiser
        self.participant = Participant.objects.filter(tournament=self.tournament)[0]
        self.url = reverse("initial_matches", kwargs={"tournament_id": self.tournament.id})

    def test_create_initial_matches_url(self):
        self.assertEqual(self.url, f"/create_initial_matches/{self.tournament.id}")

    def test_create_when_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("log_in")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_with_invalid_tournament_id(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        url = reverse("initial_matches", kwargs={"tournament_id": 999999})
        self.tournament.deadline = "2021-12-09T21:44:21.082Z"
        self.tournament.save()
        response = self.client.get(url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_when_deadline_has_not_passed_yet(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_with_tournament_which_already_has_initial_matches(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        self.tournament.deadline = "2021-12-09T21:44:21.082Z"
        self.tournament.save()
        playerA = Participant.objects.get(member=Membership.objects.get(user=1))
        playerB = Participant.objects.get(member=Membership.objects.get(user=2))
        Match.objects.create(
            tournament=self.tournament,
            playerA=playerA,
            playerB=playerB,
        )
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_when_not_an_organiser_or_coorganiser(self):
        self.client.login(email=self.participant.member.user.email, password="Password123")
        self.tournament.deadline = "2021-12-09T21:44:21.082Z"
        self.tournament.save()
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_create_when_number_of_participants_is_less_than_2(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        self.tournament.deadline = "2021-12-09T21:44:21.082Z"
        self.tournament.save()
        Participant.objects.filter(tournament=self.tournament)[0].delete()
        response = self.client.get(self.url, follow=True)
        messages = response.context["messages"]
        self.assertTrue(len(messages), 1)
        redirect_url = reverse("show_club", kwargs={"club_id": self.tournament.club.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_create_initial_matches(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        self.tournament.deadline = "2021-12-09T21:44:21.082Z"
        self.tournament.save()
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)