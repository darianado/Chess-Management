"""Unit tests of the profile form."""
from django import forms
from django.test import TestCase
from clubs.forms import EditProfileForm
from clubs.models import User

class EditProfileFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'clubs/tests/fixtures/default_user_jane.json'
    ]

    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.org',
            'bio': "Hi I'm John",
            "personal_statement": "mie imi place sa joc.",
            "chess_experience_level": 3,


        }

    def test_form_has_necessary_fields(self):
        form = EditProfileForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('bio', form.fields)
        self.assertIn('personal_statement', form.fields)
        self.assertIn('chess_experience_level', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))


    def test_valid_edit_profile_form(self):
        form = EditProfileForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['email'] = 'kcl'
        form = EditProfileForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(email='janedoe@example.org')
        form = EditProfileForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.chess_experience_level, 3)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'johndoe@example.org')
        self.assertEqual(user.bio, "Hi I'm John")
        self.assertEqual(user.personal_statement, "mie imi place sa joc.")
