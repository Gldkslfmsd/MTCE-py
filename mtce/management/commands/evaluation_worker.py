from django.core.management.base import BaseCommand

from mtce.models import *

import os

PID = os.getpid()
import sys

# TODO: one day we should start using logging correctly...
#import logging

def info(msg, *a):
#    logging.debug("Evaluation worker %d: %s" % (PID,msg))
    print("Evaluation worker %d: %s" % (PID,msg), *a)


class Command(BaseCommand):

    help = "Evaluation worker"

    def handle(self, *args, **options):
        info("started")
        while True:
            jobs = EvalJob.acquire_pack_of_jobs(100)
            if jobs == []:
                info("no available job, ending")
                break
            info("jobs %s acquired " % jobs)
            for job in jobs:
                job.launch()
                info("job %s finished" % job)
        info("evaluation worker ends")
        sys.exit(0)




