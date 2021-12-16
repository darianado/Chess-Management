from django.test import TestCase, override_settings
from clubs.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

class UserModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json"
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
    
    def test_valid_user(self):
        self._assert_user_is_valid()


# first name tests


    def test_first_name_must_not_be_blank(self):
        self.userJohn.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        self.userJohn.first_name = self.userJane.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.userJohn.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.userJohn.first_name = 'x' * 51
        self._assert_user_is_invalid()


# last name tests


    def test_last_name_must_not_be_blank(self):
        self.userJohn.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        self.userJohn.last_name = self.userJane.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.userJohn.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.userJohn.last_name = 'x' * 51
        self._assert_user_is_invalid()


# email tests


    def test_email_must_not_be_blank(self):
        self.userJohn.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        self.userJohn.email = self.userJane.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.userJohn.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.userJohn.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.userJohn.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.userJohn.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.userJohn.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


# bio tests

    def test_bio_may_be_blank(self):
        self.userJohn.bio = ''
        self._assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        self.userJohn.bio = self.userJane.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_260_characters(self):
        self.userJohn.bio = 'x' * 260
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_260_characters(self):
        self.userJohn.bio = 'x' * 261
        self._assert_user_is_invalid()


# chess experience tests


    def test_chess_experience_not_more_than_5(self):
        self.userJohn.chess_experience_level = 6
        self._assert_user_is_invalid()

    def test_chess_experience_not_less_than_1(self):
        self.userJohn.chess_experience_level = 0
        self._assert_user_is_invalid()

    def test_chess_need_not_be_unique(self):
        self.userJohn.chess_experience_level = self.userJane.chess_experience_level
        self._assert_user_is_valid()


# personal statement tests
    
    def test_ps_may_be_blank(self):
        self.userJohn.personal_statement = ''
        self._assert_user_is_valid()

    def test_ps_need_not_be_unique(self):
        self.userJohn.personal_statement = self.userJane.personal_statement
        self._assert_user_is_valid()

    def test_ps_may_contain_520_characters(self):
        self.userJohn.personal_statement = 'x' * 520
        self._assert_user_is_valid()

    def test_ps_must_not_contain_more_than_520_characters(self):
        self.userJohn.personal_statement = 'x' * 521
        self._assert_user_is_invalid()


# Create super user tests

    def test_create_super_user_but_is_staff_is_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="valid@example.org", password="Password123", is_staff=False)

    def test_create_super_user_but_is_superuser_is_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="valid@example.org", password="Password123", is_superuser=False)

    def test_create_super_user_with_no_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(password="Password123")

    def test_create_super_user(self):
        user = User.objects.create_superuser(email="valid@example.org", password="Password123")

    def _assert_user_is_valid(self):
        try:
            self.userJohn.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.userJohn.full_clean()
