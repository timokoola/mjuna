from django.core.management.base import BaseCommand, CommandError
from mapi.importers import import_all_trains

class Command(BaseCommand):
    help = 'Imports all trains moving and stores them to database (mostly for testing)'

    def handle(self, *args, **options):
        import_all_trains()
