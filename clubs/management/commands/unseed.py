from django.core.management.base import BaseCommand, CommandError
from clubs import models

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self,*arg,**options):
        models.Club.objects.all().delete()
        models.User.objects.all().delete()
        models.Members.objects.all().delete()