from django.core.management.base import BaseCommand, CommandError
from clubs import models
from faker import Faker
class Command(BaseCommand):
    """The database seeder."""
    def __init__(self):
        super().__init__()
        self.faker= Faker("en_GB")

    def handle(self, *args, **options):
        for _ in range(5):
           models.Club.objects.create(club_name = self.faker.user_name(),
                                location = self.faker.address(),
                                description=self.faker.paragraph())
        for _ in range(10):
            models.User.objects.create(first_name = self.faker.first_name(),
                                last_name = self.faker.last_name(),
                                email=self.faker.ascii_free_email(),
                                bio=self.faker.paragraph(),
                                chess_experience_level = 4)
        users =models.User.objects.all() 
        clubs= models.Club.objects.all()
        for tuser in users.iterator():
            models.Members.objects.create(club = clubs.get(id=101),
                                        user = tuser )
        
        members= models.Members.objects.all()
        for m in members.iterator():
            print(m.id)
            print(m.club.id)
            print(m.user.id)
            print(" ")