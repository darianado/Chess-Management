from django.core.management.base import BaseCommand
from clubs.models import Members

class Command(BaseCommand):
      """The database member unseeder."""

      def handle(self, *args, **options):
          Members.objects.all().delete()
