from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from clubs.models import User, Club, Membership
import random
from django.db.models import Q

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100
    MEMBER_COUNT = 50

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_clubs()
        self.create_memberships()

    def create_users(self):
        self._create_jed()
        self._create_val()
        self._create_billie()
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self._create_user()
            except (IntegrityError):
                continue
            user_count += 1

        print('User seeding complete')

    def create_clubs(self):
        description1 = self.faker.text(max_nb_chars=260)
        Club.objects.create(
            club_name = 'Kerbal Chess Club',
            location = 'SE1 4XA',
            description=description1,
        )

        description2 = self.faker.text(max_nb_chars=260)
        Club.objects.create(
            club_name = 'Borough Chess Club',
            location = 'SE1 3XA',
            description=description2,
        )

        description3 = self.faker.text(max_nb_chars=260)
        Club.objects.create(
            club_name = 'Leon Paul Chess Club',
            location = 'SW1 3XA',
            description=description3,
        )

        description4 = self.faker.text(max_nb_chars=260)
        Club.objects.create(
                club_name = 'Wild Horses Chess Club',
                location = 'SW1 3XA',
                description=description4,
                )

        print('Club seeding complete')

    def create_memberships(self):
        self._init_memberships()
        self._create_required_memberships()

        # Creating owners for the other 3 clubs
        self._create_member(random.choice(self.users), self.kerbal, 1)
        self._create_member(random.choice(self.users), self.borough, 1)
        self._create_member(random.choice(self.users), self.wild, 1)

        # Creating random memberships
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

        print('Member seeding complete')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = self.faker.unique.email()
        bio = self.faker.text(max_nb_chars=260)
        chess_experience_level = random.randint(1,5)
        personal_statement = self.faker.text(max_nb_chars=520)
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
            bio=bio,
            chess_experience_level=chess_experience_level,
            personal_statement=personal_statement,
        )

    def _create_jed(self):
        first_name = 'Jebediah'
        last_name ='Kerman'
        email = 'jeb@example.org'
        bio = self.faker.text(max_nb_chars=260)
        chess_experience_level = random.randint(1,5)
        personal_statement = self.faker.text(max_nb_chars=520)
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
            bio=bio,
            chess_experience_level=chess_experience_level,
            personal_statement=personal_statement,
        )

    def _create_val(self):
        first_name = 'Valentina'
        last_name ='Kerman'
        email = 'val@example.org'
        bio = self.faker.text(max_nb_chars=260)
        chess_experience_level = random.randint(1,5)
        personal_statement = self.faker.text(max_nb_chars=520)
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
            bio=bio,
            chess_experience_level=chess_experience_level,
            personal_statement=personal_statement,
        )

    def _create_billie(self):
        first_name = 'Billie'
        last_name ='Kerman'
        email = 'billie@example.org'
        bio = self.faker.text(max_nb_chars=260)
        chess_experience_level = random.randint(1,5)
        personal_statement = self.faker.text(max_nb_chars=520)
        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=Command.PASSWORD,
            bio=bio,
            chess_experience_level=chess_experience_level,
            personal_statement=personal_statement,
        )

    def _create_required_memberships(self):
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
        Membership.objects.create(
            user=user,
            club=club,
            role=role,
        )

    def _init_memberships(self):
        self.jed = User.objects.get(email="jeb@example.org")
        self.val = User.objects.get(email="val@example.org")
        self.billie = User.objects.get(email="billie@example.org")

        self.users = User.objects.filter(~(Q(email=self.jed.email) | Q(email=self.val.email) | Q(email=self.billie.email)))
        self.kerbal = Club.objects.get(club_name="Kerbal Chess Club")
        self.borough = Club.objects.get(club_name="Borough Chess Club")
        self.leon = Club.objects.get(club_name="Leon Paul Chess Club")
        self.wild = Club.objects.get(club_name="Wild Horses Chess Club")
