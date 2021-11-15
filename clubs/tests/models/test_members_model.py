from django.test import TestCase
from clubs.models import Club, Members, User
from django.core.exceptions import ValidationError

class MembersModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog.',
            chess_experience_level=1,
            personal_statement='nu mi place sa joc sah'
        )

        self.club = Club.objects.create(
            club_name="Cool kids club",
            location="Somewhere",
            description="Cool kids only"
        )

        self.member = Members.objects.create(
            club=self.club,
            user=self.user
        )
    
    def test_valid_member(self):
        self._assert_member_is_valid()

    def test_club_cannot_be_empty(self):
        self.member.club = None
        self._assert_member_is_invalid()

    def test_user_cannot_be_empty(self):
        self.member.user = None
        self._assert_member_is_invalid()

    def test_role_cannot_be_empty(self):
        self.member.role = None
        self._assert_member_is_invalid()

    def test_role_can_be_1(self):
        self.member.role = 1
        self._assert_member_is_valid()

    def test_role_cannot_be_0(self):
        self.member.role = 0
        self._assert_member_is_invalid()

    def test_role_cannot_be_5(self):
        self.member.role = 0
        self._assert_member_is_invalid()

    def test_user_is_only_a_member_of_a_club_exactly_once(self):
        member_2 = Members.objects.create(
            club=self.club,
            user=self.user
        )
        self._assert_member_is_invalid()

    def _assert_member_is_valid(self):
        try:
            self.member.full_clean()
        except (ValidationError):
            self.fail('Test member should be valid')

    def _assert_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.member.full_clean()
