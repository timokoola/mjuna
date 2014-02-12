# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from mapi.importers import *


class Command(BaseCommand):
    help = 'Imports all stations and stores them to database'

    def handle(self, *args, **options):
        import_stations()
        
