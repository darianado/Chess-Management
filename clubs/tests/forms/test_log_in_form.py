"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from clubs.forms import LogInForm
from clubs.models import User
from django.urls import reverse
from clubs.tests.helper import LogInTester

class LogInFormTestCase(TestCase, LogInTester):
    """Unit tests of the log in form."""
    def setUp(self):
        self.url = reverse('log_in')
        User.objects.create_user(
            first_name='Xiangyi',
            last_name='Liu',
            email='xiangyi@gmail.com',
            password='Password123',
            bio='Hi!! My name is Xiangyi.',
            chess_experience_level='1',
            personal_statement='Hello everyone!'
        )



    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/' )

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = {'email': 'xiangyi@gmail.com', 'password': 'WrongPassword123'}
        response = self.client.get(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_log_in(self):
        form_input = {'email': 'xiangyi@gmail.com', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'home.html')
