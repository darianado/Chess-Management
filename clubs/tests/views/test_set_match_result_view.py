from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from clubs.forms import SetMatchResultForm
from clubs.helpers import Status

from clubs.models import Match, Membership
from clubs.tests.helper import reverse_with_next
from clubs.views import password

class SetMatchResultViewTestCase(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/other_users.json",
        "clubs/tests/fixtures/other_memberships.json",
        "clubs/tests/fixtures/default_membership_jane_hame.json",
        "clubs/tests/fixtures/default_membership_john_hame.json",
        "clubs/tests/fixtures/default_tournament_hame.json",
        "clubs/tests/fixtures/default_participant_john.json",
        "clubs/tests/fixtures/default_participant_jane.json",
        "clubs/tests/fixtures/default_match_john_jane.json",
    ]

    def setUp(self):
        self.matchOne = Match.objects.get(id=1)
        self.url = reverse("set_match_result", kwargs={"match_id": self.matchOne.id})
        self.organiser = self.matchOne.tournament.organiser
        self.form_input = {
            "match_status": Status.WON_A.value
        }

    def test_set_match_result_url(self):
        self.assertEqual(self.url, f"/set_match_result/{self.matchOne.id}")

    def test_get_set_match_result_when_not_logged_in(self):
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse_with_next("log_in", self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_set_match_result_when_logged_in_but_not_an_organiser_or_co(self):
        officer = Membership.objects.get(id=8)
        self.client.login(email=officer.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.matchOne.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_set_match_result_when_match_id_is_invalid(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        url = reverse("set_match_result", kwargs={"match_id": 99999})
        response = self.client.get(url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_set_match_result(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'set_match_result.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SetMatchResultForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(form["match_status"].value()  , self.matchOne.match_status)

    def test_post_set_match_result_with_invalid_form(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        self.form_input["match_status"] = 999
        self.assertEqual(self.matchOne.match_status, Status.NOT_PLAYED.value)
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'set_match_result.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SetMatchResultForm))
        self.assertTrue(form.is_bound)
        self.assertEqual(self.matchOne.match_status, Status.NOT_PLAYED.value)

    def test_post_set_match_result(self):
        self.client.login(email=self.organiser.user.email, password="Password123")
        self.assertEqual(self.matchOne.match_status, Status.NOT_PLAYED.value)
        response = self.client.post(self.url, self.form_input, follow=True)
        redirect_url = reverse("show_tournament", kwargs={"tournament_id": self.matchOne.tournament.id})
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_tournament.html')
        self.matchOne.refresh_from_db()
        self.assertEqual(self.matchOne.match_status, Status.WON_A.value)
