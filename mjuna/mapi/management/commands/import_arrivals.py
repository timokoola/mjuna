# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from mapi.importers import import_arrivals

class CommandError(Exception):
    pass

class Command(BaseCommand):
    args = '<traing guid>'
    help = 'Imports specific train arrivals or for specific trains if arguments'

    def handle(self, *args, **options):
        if args:
            for train in args:
                import_arrivals(train)
        else:
            raise CommandError
