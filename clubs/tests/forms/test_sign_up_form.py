"""Tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from clubs.forms import SignUpForm
from clubs.models import User
from clubs.tests.helper import LogInTester
from django import forms


class SignUpViewTestCase(TestCase, LogInTester):
    """"Tests of the sign up form"""
    def setUp(self):
        self.form_input = {
            'first_name':'Xiangyi',
            'last_name' : 'Liu',
            'email' : 'xiangyi@gmail.com',
            'bio' : 'My bio is here',
            'chess_experience_level': '1',
            'personal_statement': 'Hi! My name is Xiangyi Liu, you can just call me Jerry',
            'new_passwords':'Password123',
            'password_confirmation': 'Password123'
        }

    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("email", form.fields)
        self.assertIn("chess_experience_level", form.fields)
        self.assertIn("personal_statement", form.fields)
        email_field = form.fields["email"]
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn("bio", form.fields)
        self.assertIn("new_passwords", form.fields)
        new_passwords_widget = form.fields["new_passwords"].widget
        self.assertTrue(isinstance(new_passwords_widget, forms.PasswordInput))
        self.assertIn("password_confirmation", form.fields)
        new_password_widget = form.fields["password_confirmation"].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_input["email"] = "xiangyi"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input["new_passwords"] = "password123"
        self.form_input["password_confirmation"] = "password123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input["new_passwords"] = "PASSWORD123"
        self.form_input["password_confirmation"] = "PASSWORD123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input["new_passwords"] = "PasswordABC"
        self.form_input["password_confirmation"] = "PasswordABC"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_and_password_confirmation_are_identical(self):
        self.form_input["password_confirmation"] = "WrongPassword123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        before_count = User.objects.count()
        form = SignUpForm(data=self.form_input)
        form.save()
        after_count = User.objects.count()
        self.assertEqual(before_count + 1, after_count)
        user = User.objects.get(email="xiangyi@gmail.com")
        self.assertEqual(user.first_name, "Xiangyi")
        self.assertEqual(user.last_name, "Liu")
        self.assertEqual(user.chess_experience_level, 1)
        self.assertEqual(user.bio, "My bio is here")
        self.assertTrue(check_password("Password123", user.password))
