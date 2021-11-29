from clubs.models import Members, Club, User
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.db.models import Q
import random

class Command(BaseCommand):
    MEMBER_COUNT = 50

    def __init__(self):
        super().__init__()
        self.jed = User.objects.get(email="jeb@example.org")
        self.val = User.objects.get(email="val@example.org")
        self.billie = User.objects.get(email="billie@example.org")

        self.users = User.objects.filter(~(Q(email=self.jed.email) | Q(email=self.val.email) | Q(email=self.billie.email)))
        self.kerbal = Club.objects.get(club_name="Kerbal Chess Club")
        self.borough = Club.objects.get(club_name="Borough Chess Club")
        self.leon = Club.objects.get(club_name="Leon Paul Chess Club")
        self.wild = Club.objects.get(club_name="Wild Horses Chess Club")

    def handle(self, *args, **options):
        self._create_members()
        print('Member seeding complete')

    def _create_members(self):
        self._create_required_members()

        # Creating owners for the other 3 clubs
        self._create_member(random.choice(self.users), self.kerbal, 1)
        self._create_member(random.choice(self.users), self.borough, 1)
        self._create_member(random.choice(self.users), self.wild, 1)

        # Creating random members
        member_count = 0
        while member_count < Command.MEMBER_COUNT:
            try:
                self._create_member(random.choice(self.users), self.kerbal, random.randint(2, 4))
                member_count += 1
                self._create_member(random.choice(self.users), self.borough, random.randint(2, 4))
                member_count += 1
                self._create_member(random.choice(self.users), self.leon, random.randint(2, 4))
                member_count += 1
                self._create_member(random.choice(self.users), self.wild, random.randint(2, 4))
                member_count += 1
            except IntegrityError:
                continue
    
    def _create_required_members(self):
        # All three users are members of kerbal
        self._create_member(self.jed, self.kerbal, 3)
        self._create_member(self.val, self.kerbal, 3)
        self._create_member(self.billie, self.kerbal, 3)

        # jed is an officer of borough
        self._create_member(self.jed, self.borough, 2)

        # val is the owner of leon
        self._create_member(self.val, self.leon, 1)

        # billie is a member of wild
        self._create_member(self.billie, self.wild, 3)

    def _create_member(self, user, club, role=3):
        Members.objects.create(
            user=user,
            club=club,
            role=role,
        )
