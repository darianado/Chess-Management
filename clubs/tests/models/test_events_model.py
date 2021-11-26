from django.test import TestCase
from clubs.models import Club, Members, User, Events
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class EventsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Xiangyi',
            last_name='Liu',
            email='xiangyi@gmail.com',
            password='Password123',
            bio='Hi!',
            chess_experience_level=2,
            personal_statement='Hi!'
        )

        self.club = Club.objects.create(
            club_name="Kings club",
            location="EC1N",
            description="Club for Kings students"
        )

        self.action = Events.objects.create(
            club=self.club,
            user=self.user
        )

    def test_valid_action(self):
        self._assert_action_is_valid()

    def test_club_cannot_be_empty(self):
        self.action.club = None
        self._assert_member_is_invalid()

    def test_user_cannot_be_empty(self):
        self.action.user = None
        self._assert_member_is_invalid()


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
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                club=self.club,
                user=self.user
            )

    def _assert_member_is_valid(self):
        try:
            self.member.full_clean()
        except (ValidationError):
            self.fail('Test member should be valid')

    def _assert_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.member.full_clean()
