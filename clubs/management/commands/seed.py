from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from clubs.models import Match, Participant, Tournament, User, Club, Membership
from clubs.helpers import Role
import random
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, time, timedelta

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
        self.create_tournaments()
        self.create_participants()
        self.create_matches()

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

        # Creating owners for the other 2 clubs
        self._create_member(random.choice(self.users), self.borough, Role.OWNER)
        self._create_member(random.choice(self.users), self.wild, Role.OWNER)

        # Creating random memberships
        member_count = 0
        while member_count < Command.MEMBER_COUNT:
            try:
                self._create_member(random.choice(self.users), self.kerbal, random.randint(Role.OFFICER, Role.APPLICANT))
                member_count += 1
                self._create_member(random.choice(self.users), self.borough, random.randint(Role.OFFICER, Role.APPLICANT))
                member_count += 1
                self._create_member(random.choice(self.users), self.leon, random.randint(Role.OFFICER, Role.APPLICANT))
                member_count += 1
                self._create_member(random.choice(self.users), self.wild, random.randint(Role.OFFICER, Role.APPLICANT))
                member_count += 1
            except IntegrityError:
                continue

        print('Member seeding complete')

    def create_tournaments(self):
        self._create_required_tournaments()

        print("Tournament seeding complete")

    def create_participants(self):
        self._create_required_participants()

        participants = Membership.objects.filter(club=self.kerbal, role=Role.MEMBER).exclude(user=self.jed)
        for participant in participants:
            self._create_participant(self.tourny, participant)

        print("Participant seeding complete")

    def create_matches(self):
        #TODO: Seed some matches
        print("Matches seeding complete")

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
        self._create_member(self.jed, self.kerbal, Role.MEMBER)
        self._create_member(self.val, self.kerbal, Role.OFFICER)
        self._create_member(self.billie, self.kerbal, Role.OWNER)

        # jed is an officer of borough
        self._create_member(self.jed, self.borough, Role.OFFICER)

        # val is the owner of leon
        self._create_member(self.val, self.leon, Role.OWNER)

        # billie is a member of wild
        self._create_member(self.billie, self.wild, Role.MEMBER)

    def _create_required_tournaments(self):
        organiser = Membership.objects.get(user=self.val, club=self.kerbal)

        Tournament.objects.create(
            name="Kerbal Chess Club Tournament",
            description="Welcome to our tournament!",
            deadline=datetime.isoformat(datetime.now(tz=timezone.utc) + timedelta(days=1)),
            organiser=organiser,
            club=self.kerbal,
        )

        self.tourny = Tournament.objects.create(
            name="Kerbal Chess Club Tournament 2",
            description="Welcome to our tournament again!",
            deadline=datetime.isoformat(datetime.now(tz=timezone.utc) - timedelta(hours=1)),
            organiser=organiser,
            club=self.kerbal,
        )

    def _create_required_participants(self):
        jed = Membership.objects.get(user=self.jed, club=self.kerbal)
        self._create_participant(self.tourny, jed)

    def _create_participant(self, tournament, member):
        Participant.objects.create(
            tournament=tournament,
            member=member,
        )

    def _create_match(self, tournament, playerA, playerB):
        Match.objects.create(
            tournament=tournament,
            playerA=playerA,
            playerB=playerB
        )

    def _create_member(self, user, club, role=Role.MEMBER):
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
