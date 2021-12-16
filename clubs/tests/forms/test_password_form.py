"""Unit tests of the edit password form."""
from django import forms
from django.test import TestCase
from clubs.models import User
from clubs.forms import changePasswordForm

class PasswordFormTestCase(TestCase):
    """Unit tests of the edit password form."""

    def setUp(self):
        self.form_input = {
            'old_password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    def test_form_has_necessary_fields(self):
        form = changePasswordForm()
        self.assertIn('old_password', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)

    def test_form_fields_are_using_password_input_widgets(self):
        form = changePasswordForm()
        self.assertTrue(isinstance(form.fields["old_password"].widget, forms.PasswordInput))
        self.assertTrue(isinstance(form.fields["new_password"].widget, forms.PasswordInput))
        self.assertTrue(isinstance(form.fields["password_confirmation"].widget, forms.PasswordInput))

    def test_valid_form(self):
        form = changePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        self.form_input['password_confirmation'] = 'PasswordABC'
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_old_password(self):
        self.form_input["old_password"] = ""
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_new_password(self):
        self.form_input["new_password"] = ""
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password_confirmation(self):
        self.form_input["password_confirmation"] = ""
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_old_password_equal_to_new_password(self):
        self.form_input["old_password"] = self.form_input["new_password"]
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
