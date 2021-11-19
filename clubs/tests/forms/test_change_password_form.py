from django import forms
from django.test import TestCase

from clubs.forms import changePasswordForm

class ChangePasswordFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            "old_password": "Password123",
            "new_password": "Password1234",
            "password_confirmation": "Password1234",
        }

    def test_form_contains_required_fields(self):
        form = changePasswordForm()
        self.assertIn("old_password", form.fields)
        self.assertIn("new_password", form.fields)
        self.assertIn("password_confirmation", form.fields)
        
        self.assertTrue(isinstance(form.fields["old_password"].widget, forms.PasswordInput))
        self.assertTrue(isinstance(form.fields["new_password"].widget, forms.PasswordInput))
        self.assertTrue(isinstance(form.fields["password_confirmation"].widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = changePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

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
        self.form_input["old_password"] = "Password1234"
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input["password_confirmation"] = "WrongPassword123"
        form = changePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())
