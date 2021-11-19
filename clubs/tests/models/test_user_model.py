from django.test import TestCase, override_settings
from clubs.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

import tempfile
import shutil

# ImageField testing taken from here https://stackoverflow.com/a/61672120

MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserModelTest(TestCase):
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.user = User.objects.create_user(
        '@johndoe',
        first_name='John',
        last_name='Doe',
        email='johndoe@example.org',
        password='Password123',
        bio='The quick brown fox jumps over the lazy dog.',
        chess_experience_level= 1,
        personal_statement= 'nu mi place sa joc sah',
        )
    
    def test_valid_user(self):
        self._assert_user_is_valid()


# username tests

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user.username = '@'  +  'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@'  +  'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user.username = '@@johndoe'
        self._assert_user_is_invalid()


# first name tests


    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


# last name tests


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()


# email tests


    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


# bio tests

    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_260_characters(self):
        self.user.bio = 'x' * 260
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_260_characters(self):
        self.user.bio = 'x' * 261
        self._assert_user_is_invalid()


# chess experience tests


    def test_chess_experience_not_more_than_5(self):
        self.user.chess_experience_level = 6
        self._assert_user_is_invalid()

    def test_chess_experience_not_less_than_1(self):
        self.user.chess_experience_level = 0
        self._assert_user_is_invalid()

    def test_chess_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.chess_experience_level = second_user.chess_experience_level
        self._assert_user_is_valid()


# personal statement tests
    
    def test_ps_may_be_blank(self):
        self.user.personal_statement = ''
        self._assert_user_is_valid()

    def test_ps_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.personal_statement = second_user.personal_statement
        self._assert_user_is_valid()

    def test_ps_may_contain_520_characters(self):
        self.user.personal_statement = 'x' * 520
        self._assert_user_is_valid()

    def test_ps_must_not_contain_more_than_520_characters(self):
        self.user.personal_statement = 'x' * 521
        self._assert_user_is_invalid()


# gravatar upload tests

    def test_gravatar_can_be_blank(self):
        self.user.gravatar = None
        self._assert_user_is_valid()




    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
        '@janedoe',
        first_name='Jane',
        last_name='Doe',
        email='janedoe@example.org',
        password='Password123',
        bio="This is Jane's profile.",
        chess_experience_level= 3,
        personal_statement= 'mie imi place sa joc sah!'
        )
        return user