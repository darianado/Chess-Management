from django.test import TestCase
from clubs.models import Club, Members, User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.db import transaction

from clubs.helpers import Role

class MembersModelTest(TestCase):

    fixtures = [
        "clubs/tests/fixtures/default_user_john.json",
        "clubs/tests/fixtures/default_user_jane.json",
        "clubs/tests/fixtures/default_user_mark.json",
        "clubs/tests/fixtures/default_club_hamersmith.json",
        "clubs/tests/fixtures/default_club_hame.json",
        "clubs/tests/fixtures/default_member_john_hame.json",
        "clubs/tests/fixtures/default_member_jane_hame.json",
        "clubs/tests/fixtures/default_member_mark_hame.json",
    ]

    def setUp(self):
        self.userJohn = User.objects.get(email="johndoe@example.org")
        self.userJane = User.objects.get(email="janedoe@example.org")
        self.userMark = User.objects.get(email="Markvue@example.org")
        self.clubHame = Club.objects.get(club_name="Hame Chess Club")
        self.memberJohn = Members.objects.get(club=self.clubHame, user=self.userJohn)
        self.memberJane = Members.objects.get(club=self.clubHame, user=self.userJane)
        self.memberMark = Members.objects.get(club=self.clubHame, user=self.userMark)

    def test_valid_member(self):
        self._assert_member_is_valid()

    def test_club_cannot_be_empty(self):
        self.memberJane.club = None
        self._assert_member_is_invalid()

    def test_user_cannot_be_empty(self):
        self.memberJane.user = None
        self._assert_member_is_invalid()

    def test_role_cannot_be_empty(self):
        self.memberJane.role = None
        self._assert_member_is_invalid()

    def test_role_can_be_1(self):
        self.memberJane.role = 1
        self._assert_member_is_valid()

    def test_role_cannot_be_0(self):
        self.memberJane.role = 0
        self._assert_member_is_invalid()

    def test_role_cannot_be_5(self):
        self.memberJane.role = 5
        self._assert_member_is_invalid()

    def test_user_is_only_a_member_of_a_club_exactly_once(self):
        with self.assertRaises(IntegrityError):
            Members.objects.create(
                club=self.clubHame,
                user=self.userJane
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
            self.memberJane.full_clean()
        except (ValidationError):
            self.fail('Test member should be valid')

    def _assert_member_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.memberJane.full_clean()

    def test_acceptApplicant_successful(self):
        role = self.memberMark.role
        if role!=4:
            self.fail('Test member should be Applicant')
        else:
            self.memberMark.acceptApplicant()
            self.assertEqual(self.memberMark.role, 3)

    def test_denyApplicant_successful(self):
        role = self.memberMark.role
        if role!=4:
            self.fail('Test member should be Applicant')
        else:
            self.memberMark.denyApplicant()
            try:
                member = Members.objects.get(club=self.clubHame, user=self.userMark)
            except(ObjectDoesNotExist):
                member = None
            self.assertEqual(member,None)

    def test_demote_successful(self):
        before_role = self.memberJane.role
        self.memberJane.demote()
        self.assertEqual(self.memberJane.role, before_role+1)

    def test_promote_successful(self):
        before_role = self.memberJohn.role
        self.memberJohn.promote()
        self.assertEqual(self.memberJohn.role, before_role-1)

    def test_member_kick_successful(self):
        self.memberJohn.member_kick()
        try:
            member = Members.objects.get(club=self.clubHame, user=self.userJohn)
        except(ObjectDoesNotExist):
            member = None
        self.assertEqual(member,None)
