from django.core.management.base import BaseCommand, CommandError
from clubs import models

class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self,*arg,**options):
        models.Match.objects.all().delete()
        models.Participant.objects.all().delete()
        models.Tournament.objects.all().delete()
        models.Membership.objects.all().delete()
        models.Club.objects.all().delete()
        models.User.objects.filter(is_staff=False, is_superuser=False).delete()
