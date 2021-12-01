from django.test import TestCase
from clubs.models import Club, Members, User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction

from clubs.helpers import Role

class MembersModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_member_john_hame.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.member = Members.objects.get(club=self.clubHame, user=self.userJohn)
        self.member.role = 1
        self.member.save()
    
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
                club=self.clubHame,
                user=self.userJohn
            )

    def test_a_club_cannot_have_more_than_1_owner(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Members.objects.create(
                    club=self.clubHame,
                    user=self.userJane,
                    role=Role.OWNER
                )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                member = Members.objects.create(
                    club=self.clubHame,
                    user=self.userJane,
                    role=Role.MEMBER
                )
                member.role = 1
                member.save()

    def _assert_member_is_valid(self):
        try:
            self.member.full_clean()
        except (ValidationError):
            self.fail('Test member should be valid')

    def _assert_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.member.full_clean()
