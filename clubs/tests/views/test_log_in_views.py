"""Tests of the log in view."""
from django.test import TestCase
from clubs.forms import LogInForm
from django.urls import reverse
from clubs.models import User
from clubs.tests.helper import LogInTester, reverse_with_next
from django.contrib import messages

class LogInViewTestCase(TestCase, LogInTester):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json"
    ]

    """"Tests of the log in view."""
    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(email="johndoe@example.org")

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/' )

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse("show_user")
        self.url = reverse_with_next("log_in", destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "log_in.html")
        form = response.context["form"]
        next = response.context["next"]
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)

    def test_unsuccessful_log_in(self):
        form_input = {
            'email': 'johndoe@example.org',
            'password': 'WrongPassword123'
        }
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {
            'email': 'johndoe@example.org',
            'password': 'Password123'
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'partials/dashboard.html')

    def test_successful_log_in_with_redirect(self):
        redirect_url = reverse("show_user")
        form_input = {
            "email": "johndoe@example.org",
            "password": "Password123",
            "next": redirect_url
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "show_user.html")

    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        response_url = reverse("home")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

    def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.email, password="Password123")
        form_input = {
            "email": "fakeemail@example.org",
            "password": "WrongPassword123"
        }
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse("home")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "home.html")

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {
            'email': 'johndoe@example.org',
            'password': 'Password123'
        }
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('show_user')
        form_input = { 'email': 'johndoe@example.org', 'password': 'WrongPassword123', 'next': redirect_url }
        response = self.client.post(self.url, form_input)
        next = response.context['next']
        self.assertEqual(next, redirect_url)
