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
        "clubs/tests/fixtures/default_member_jane_hame.json",
        "clubs/tests/fixtures/other_users.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.userCharlie = User.objects.get(email="charliedoe@example.org")

        self.clubHame = Club.objects.get(club_name="Hame Chess Club")

        self.member = Members.objects.get(club=self.clubHame, user=self.userJohn)
        self.memberJane = Members.objects.get(club=self.clubHame, user=self.userJane)

        self.member.role = 1
        self.memberJane.role = 2
        
        self.memberJane.save()
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

    def test_get_correct_role_name_owner(self):
        role_member_john = Members.get_member_role_name(Members.get_member_role(self.userJohn, self.clubHame))
        self.assertEqual(role_member_john, "Owner")

    def test_get_correct_role_name_member(self):
        self.member.role = 3
        self.member.save()

        role_member_john = Members.get_member_role_name(Members.get_member_role(self.userJohn, self.clubHame))
        self.assertEqual(role_member_john, "Member")

    def test_get_correct_role_name_applicant(self):
        self.memberJane.role = 4
        self.memberJane.save()

        role_member_jane = Members.get_member_role_name(Members.get_member_role(self.userJane, self.clubHame))
        self.assertEqual(role_member_jane, "Applicant")

    def test_get_correct_role_name_officer(self):
        role_member_jane = Members.get_member_role_name(Members.get_member_role(self.userJane, self.clubHame))
        self.assertEqual(role_member_jane, "Officer")

    def test_get_incorrect_role_name(self):
        self.member.role = 0
        self.member.save()

        role_member_john = Members.get_member_role_name(Members.get_member_role(self.userJohn, self.clubHame))
        self.assertEqual(role_member_john, "")

    def test_get_correct_role_name_user(self):
        role_member_charlie = Members.get_member_role_name(Members.get_member_role(self.userCharlie, self.clubHame))
        self.assertEqual(role_member_charlie, "User")

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
