"""Tests of the sign up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from clubs.forms import SignUpForm
from django.urls import reverse
from clubs.models import User
from clubs.tests.helper import LogInTester

class SignUpViewTestCase(TestCase, LogInTester):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json"
    ]

    """"Tests of the sign up view."""
    def setUp(self):
        self.url = reverse('sign_up')
        self.form_input = {
            'first_name':'Xiangyi',
            'last_name' : 'Liu',
            'email' : 'xiangyi@gmail.com',
            'bio' : 'My bio is here',
            'chess_experience_level': '2',
            'personal_statement': 'Hi! My name is Xiangyi Liu, you can just call me Jerry',
            'new_passwords':'Password123',
            'password_confirmation': 'Password123',
        }

        self.userJohn = User.objects.get(email="johndoe@example.org")

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/' )

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)

    def test_get_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.userJohn.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "home.html")

    def test_unsuccessful_sign_up(self):
        self.form_input['email'] = 'What'
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
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'home.html')
        user = User.objects.get(email = 'xiangyi@gmail.com')
        self.assertEqual(user.first_name, 'Xiangyi')
        self.assertEqual(user.last_name, 'Liu')
        self.assertEqual(user.personal_statement, 'Hi! My name is Xiangyi Liu, you can just call me Jerry' )
        self.assertEqual(user.bio, 'My bio is here')
        self.assertEqual(user.chess_experience_level, 2)
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 1)

    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.userJohn.email, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        redirect_url = reverse("dashboard")
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "home.html")
