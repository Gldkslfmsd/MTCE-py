
from .background_importer import *


from django.core.management.base import BaseCommand



class Command(BaseCommand):

    help = "Whatever you want to print here"

    def add_arguments(self, parser):
        parser.add_argument('--workers', type=int, default=multiprocessing.cpu_count(),
                            help="Maximum number of worker processes for evaluation. "
                            "Default: current number of CPUs.")


    def handle(self, *args, **options):
        print(args)
        print(options)

        workers = options['workers']

        infinite=True

        em = EvaluationManager(workers=workers)
        while True:
            importing_loop_iteration()
    #        deleting_loop()
            em.evaluation_manager_iteration()
            if not infinite:
                break
            print()
            time.sleep(2)

