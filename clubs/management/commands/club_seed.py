from clubs.models import Club
from django.core.management.base import BaseCommand, CommandError
from faker import Faker

class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self._create_club()
        print('User seeding complete')

    def _create_club(self):
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



