from django.core.management.base import BaseCommand
from django.db import transaction
from mtce.models import *
from mtce.bootstrap import pickle_masks_cache

import time
import os
import shutil
import multiprocessing

def info(msg, *a):
    print("INFO: %s" % (msg), *a)

def import_log(msg="", *a):
    #return
    print("IMPORT:",msg, *a)

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
            with transaction.atomic():
                importing_loop_iteration()
    #        deleting_loop()
            #em.evaluation_manager_iteration()
            #pickle_masks_cache()
            if not infinite:
                break
            print()
            time.sleep(10)



base = os.path.join("files","comparisons")

def import_comparison(path):
    import_log("    importing new comparison", path)
    name = os.path.basename(path)
    src = os.path.join(path, "source.txt")
    ref = os.path.join(path, "reference.txt")
    c = Comparison(name=name,origsourcefile=src,origreferencefile=ref)
    c.save()

    for dir in os.listdir(path):
        pdir = os.path.join(path, dir)
        if os.path.isdir(pdir): # MTSystem dir
            sys = None
            for cdir in os.listdir(pdir):  # checkpoint dir
                trans = os.path.join(pdir,cdir,"translation.txt")
                if os.path.exists(trans):
                    if sys is None:
                        sys = create_MTSystem(dir,c)
                        sys.save()

                        import_log("     creating MTSystem",sys)
                    cp = create_Checkpoint(cdir,trans,sys)
                    cp.save()
#                    di = create_DataImport(trans,'translation.txt',cp)
                    import_log("     creating Checkpoint",cp)
#                    di.save()
        else:
            if dir not in ("source.txt","reference.txt"):
                import_log("ignoring extra file ",path,dir)



def check_comparison(path):
    import_log("  inside check comparison",path)
    for file in os.listdir(path):
        if file in ("source.txt", "reference.txt"):
            pfile = os.path.join(path, file)
            import_log("  needs new import:",DataImport.needs_new_import(pfile))
            if DataImport.needs_new_import(pfile):
                import_comparison(path)
                import_log("  new import:", pfile)
                return
            elif DataImport.needs_reimport(pfile):
                import_log("  proceeding reimport",pfile)
                DataImport.reimport(pfile, file)
            else:
                import_log("  reimport not needed",pfile)
#        else:
#            import_log("skipping %s" % file)

def import_checkpoint(path,sys,comp):
    try:
        c = Comparison.find_by_name(comp)
    except Comparison.DoesNotExist:
        import_log("error, missing comparison")
        return

    try:
        s = MTSystem.find_by_name(sys)
    except MTSystem.DoesNotExist:
        s = create_MTSystem(sys,c)
        s.save()

    cname = os.path.basename(path)
    t_full = os.path.join(path,"translation.txt")
    cp = create_Checkpoint(cname, t_full,s)
    cp.save()
#    di = create_DataImport(t_full,"translation.txt",cp)
#    di.save()


def check_checkpoint(path,sys=None,comp=None):
    for _,dirs,files in os.walk(path):
        if dirs:
            import_log("ignoring",dirs)
        if "translation.txt" in files:
            tran_full = os.path.join(path,"translation.txt")
            import_log("  checking checkpoint",tran_full)
            import_log("  needs new import:",DataImport.needs_new_import(tran_full))
            if DataImport.needs_new_import(tran_full):
                import_checkpoint(path,sys,comp)
            elif DataImport.needs_reimport(tran_full):
                import_log("  needs reimport: True")
                DataImport.reimport(os.path.join(path,'translation.txt'),'translation.txt')
                import_log("  reimported")
            else:
                import_log("  needs reimport: False")

        for f in files:
            if f == "translation.txt": continue
            if f.startswith("translation"):
                m = maybe_create_metatranslation(path, f)
                if m is not None:
                    m.save()



def importing_loop_iteration(infinite=True):
        import_log("importing loop iteration...")
        for _,comp_dirs,files in os.walk(base):
            for comp_dir_name in comp_dirs:
                comp_dir_full = os.path.join(base, comp_dir_name)
                import_log(" checking comparison",comp_dir_full)
                check_comparison(comp_dir_full)
                import_log(" ",comp_dir_full,"check comparison done")
                import_log()
                for _,sys_dirs,extra_files in os.walk(comp_dir_full):
                    for sys_dir_name in sys_dirs:
                        sys_dir_full = os.path.join(comp_dir_full,sys_dir_name)
                        for _,ch_dirs,_ in os.walk(sys_dir_full):
                            for ch_dir in ch_dirs:
                                ch_dir_full = os.path.join(sys_dir_full,ch_dir)
                                import_log(" checkpoint check:",ch_dir_full)
                                check_checkpoint(ch_dir_full,sys=sys_dir_name,comp=comp_dir_name)
                                import_log(" end of checkpoint check")
                                import_log()
                    break
            break



def deleting_loop(infinite=True):
    # TODO: check if this is still necessary
    # TODO -- go through the database and delete objects, whose files were deleted
    while True:
        pass
        if not infinite:
            break
        import_log()
        time.sleep(2)

import subprocess
from collections import deque
multiprocessing.log_to_stderr()

class EvaluationManager:

    def __init__(self, workers):
        self.pool = multiprocessing.Pool(workers)

        self.running_jobs = deque()

    @staticmethod
    def worker(job):
        info("job %s started, state: %s" % (job, job.state))
        job.launch()
        info("job %s finished, state: %s" % (job, job.state))
        return job

    def evaluation_manager_iteration(self):
        print("evaluation manager iteration...")
        jobs = EvalJob.acquire_pack_of_jobs(1000)
        for job in jobs:
            print("launching",job)
            res = self.pool.apply_async(self.worker, (job,))
            self.running_jobs.append(res)

        # one round around the queue to save the finished results to the database
        end_plug = "[_PLUG_]"
        self.running_jobs.append(end_plug)
        with transaction.atomic():
            while True:
                res = self.running_jobs.popleft()
                if res == end_plug:
                    break
                elif res.ready():
                    job = res.get()
                    job.save_to_db()
                else:
                    self.running_jobs.append(res)

