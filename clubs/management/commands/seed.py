# from django.core.management.base import BaseCommand, CommandError
# from clubs import models
# from faker import Faker
# class Command(BaseCommand):
#     """The database seeder."""
#     def __init__(self):
#         super().__init__()
#         self.faker= Faker("en_GB")

#     def handle(self, *args, **options):
#         for _ in range(5):
#            models.Club.objects.create(club_name = self.faker.user_name(),
#                                 location = self.faker.address(),
#                                 description=self.faker.paragraph())
#         for _ in range(10):
#             models.User.objects.create(first_name = self.faker.first_name(),
#                                 last_name = self.faker.last_name(),
#                                 email=self.faker.ascii_free_email(),
#                                 bio=self.faker.paragraph(),
#                                 chess_experience_level = 4)
#         users =models.User.objects.all() 
#         clubs= models.Club.objects.all()
#         for tuser in users.iterator():
#             models.Members.objects.create(club = clubs.get(id=101),
#                                         user = tuser )
        
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker
from clubs.models import User
import random

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self._create_user()
            except (IntegrityError):
                continue
            user_count += 1
        self._create_jed()
        self._create_val()
        self._create_billie()
        print('User seeding complete')

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
