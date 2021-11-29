from django.core.management.base import BaseCommand, CommandError
from clubs.models import Club

class Command(BaseCommand):
      """The database unseeder."""

      def handle(self, *args, **options):
          Club.objects.all().delete()
