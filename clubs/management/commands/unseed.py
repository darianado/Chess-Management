from django.core.management.base import BaseCommand, CommandError
from clubs import models

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self,*arg,**options):
        models.Club.objects.all().exclude(id=101).delete()
        models.User.objects.filter(is_staff=False, is_superuser=False).delete()
        models.Members.objects.all().delete()
