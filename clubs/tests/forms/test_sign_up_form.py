"""Tests of the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from microblogs.forms import SignUpForm
from django.urls import reverse
from microblogs.models import User
from .helper import LogInTester


class SignUpViewTestCase(TestCase, LogInTester):
    """"Tests of the sign up view."""
    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name':'Xiangyi',
            'last_name' : 'Liu',
            'username':'@Liu',
            'email' : 'xiangyi@gmail.com',
            'bio' : 'My bio is here',
            'chess_experience_level': '1',
            'new_passwords':'Password123',
            'password_confirmation': 'Password123'
        }

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/' )

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_sign_up(self):
        self.form_input['username'] = 'What'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow = True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('welcome')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'welcome.html')
        user = User.objects.get(username = '@Liu')
        self.assertEqual(user.first_name, 'Xiangyi')
        self.assertEqual(user.last_name, 'Liu')
        self.assertEqual(user.email, 'xiangyi@gmail.com')
        self.assertEqual(user.bio, 'My bio is here')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
