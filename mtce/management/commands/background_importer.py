from django.core.management.base import BaseCommand

from mtce.models import *

import time

class Command(BaseCommand):

    help = "Whatever you want to print here"

    def handle(self, *args, **options):
        print(args)
        print(options)

        run_data_importer()



def run_data_importer():
    while True:
        print("abc")
        time.sleep(1)
