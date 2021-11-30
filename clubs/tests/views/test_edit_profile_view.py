from django.test import TestCase
from clubs.models import User
from django.urls import reverse
from clubs.forms import EditProfileForm
from django.contrib import messages

from clubs.tests.helper import reverse_with_next

class EditUserProfileViewTestCase(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'clubs/tests/fixtures/default_user_john.json',
        'clubs/tests/fixtures/default_user_jane.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='johndoe@example.org')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'email': 'johndoe2@example.org',
            'bio': "Hi I'm John2",
            'chess_experience_level': 1,
            'personal_statement': 'nu mi place sa joc sah2',
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_edit_profile_when_not_logged_in(self):
        response = self.client.get(self.url)
        redirect_url = reverse_with_next("log_in", self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_profile(self):
        self.client.login(email=self.user.email, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertEqual(form.instance, self.user)

    def test_unsuccesful_profile_update(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = 'BadEmail'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "Hi I'm John")
        self.assertEqual(self.user.chess_experience_level, 1)
        self.assertEqual(self.user.personal_statement, "nu mi place sa joc sah")

    def test_unsuccessful_profile_update_due_to_duplicate_email(self):
        self.client.login(email=self.user.email, password='Password123')
        self.form_input['email'] = 'BadEmail'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditProfileForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')
        self.assertEqual(self.user.bio, "Hi I'm John")
        self.assertEqual(self.user.chess_experience_level, 1)
        self.assertEqual(self.user.personal_statement, "nu mi place sa joc sah")

    def test_succesful_profile_update(self):
        self.client.login(email=self.user.email, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('show_user', kwargs={"user_id": 1})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'show_user.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')
        self.assertEqual(self.user.email, 'johndoe2@example.org')
        self.assertEqual(self.user.bio, "Hi I'm John2")
        self.assertEqual(self.user.chess_experience_level, 1)
        self.assertEqual(self.user.personal_statement, "nu mi place sa joc sah2")

