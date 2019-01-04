from django.core.management.base import BaseCommand
from django.db import transaction
from mtce.models import *

from mtce.sentence_listing import *

class Command(BaseCommand):

    help = "Whatever you want to print here"


    def handle(self, *args, **options):

        ch = Checkpoint.objects.all().last()
        print(ch)

        get_translation_sentences(ch,True)

