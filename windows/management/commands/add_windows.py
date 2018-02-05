from django.core.management.base import BaseCommand, CommandError
from windows.models import Window
import csv
import os

class Command(BaseCommand):
    help = 'Adds a tsv of window data to the database'

    def add_arguments(self, parser):
        parser.add_argument('window_tsv')

    def handle(self, *args, **options):
        if not os.path.exists(options['window_tsv']):
            raise ValueError('{} does not exist'.format(options['window_tsv']))
        reader = csv.DictReader(open(options['window_tsv']), dialect='excel-tab')
        missing = {"Floor", "Room", "Code"} - set(reader.fieldnames)
        if missing:
            print("Fields: {} not present in input file".format(missing))
        i = 0
        for line in reader:
            w = Window(code=line['Code'], description="{} floor {}".format(
                line['Floor'], line['Room']))
            w.save()
            i += 1

        self.stdout.write(self.style.SUCCESS('Successfully wrote information on'
                                             ' {} windows to the database'.format(i)))