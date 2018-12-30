from django.core.management.base import BaseCommand

from mtce.models import *

import time
import os
import shutil
import multiprocessing

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



base = os.path.join("files","comparisons")

def import_comparison(path):
    print("    importing new comparison", path)
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

                        print("     creating MTSystem",sys)
                    cp = create_Checkpoint(cdir,trans,sys)
                    cp.save()
#                    di = create_DataImport(trans,'translation.txt',cp)
#                    print("     creating Checkpoint",cp)
#                    di.save()
        else:
            if dir not in ("source.txt","reference.txt"):
                print("ignoring extra file ",path,dir)



def check_comparison(path):
    print("  inside check comparison",path)
    for file in os.listdir(path):
        if file in ("source.txt", "reference.txt"):
            pfile = os.path.join(path, file)
            print("  needs new import:",DataImport.needs_new_import(pfile))
            if DataImport.needs_new_import(pfile):
                import_comparison(path)
                print("  new import:", pfile)
                return
            elif DataImport.needs_reimport(pfile):
                print("  proceeding reimport",pfile)
                DataImport.reimport(pfile, file)
            else:
                print("  reimport not needed",pfile)
#        else:
#            print("skipping %s" % file)

def import_checkpoint(path,sys,comp):
    try:
        c = Comparison.find_by_name(comp)
    except Comparison.DoesNotExist:
        print("error, missing comparison")
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
            print("ignoring",dirs)
        if "translation.txt" in files:
            tran_full = os.path.join(path,"translation.txt")
            print("  checking checkpoint",tran_full)
            print("  needs new import:",DataImport.needs_new_import(tran_full))
            if DataImport.needs_new_import(tran_full):
                import_checkpoint(path,sys,comp)
            elif DataImport.needs_reimport(tran_full):
                print("  needs reimport: True")
                DataImport.reimport(os.path.join(path,'translation.txt'),'translation.txt')
                print("  reimported")
            else:
                print("  needs reimport: False")


def importing_loop_iteration(infinite=True):
        print("importing loop iteration...")
        for _,comp_dirs,files in os.walk(base):
            for comp_dir_name in comp_dirs:
                comp_dir_full = os.path.join(base, comp_dir_name)
                print(" checking comparison",comp_dir_full)
                check_comparison(comp_dir_full)
                print(" ",comp_dir_full,"check comparison done")
                print()
                for _,sys_dirs,extra_files in os.walk(comp_dir_full):
                    for sys_dir_name in sys_dirs:
                        sys_dir_full = os.path.join(comp_dir_full,sys_dir_name)
                        for _,ch_dirs,_ in os.walk(sys_dir_full):
                            for ch_dir in ch_dirs:
                                ch_dir_full = os.path.join(sys_dir_full,ch_dir)
                                print(" checkpoint check:",ch_dir_full)
                                check_checkpoint(ch_dir_full,sys=sys_dir_name,comp=comp_dir_name)
                                print(" end of checkpoint check")
                                print()
                    break
            break



def deleting_loop(infinite=True):
    # TODO -- go through the database and delete objects, whose files were deleted
    while True:
        pass
        if not infinite:
            break
        print()
        time.sleep(2)

import subprocess

class EvaluationManager:

    def __init__(self, workers):
        self.running_workers = []
        self.max_workers = workers


    def evaluation_manager_iteration(self):
        print("evaluation manager iteration...")
        waiting_jobs = EvalJob.waiting_jobs().count()
#        print("waiting jobs:!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n",waiting_jobs)
        actualy_running_workers = []
        workers_to_start = min(self.max_workers,waiting_jobs)
        print(self.running_workers)
        for w in self.running_workers:
            print(w,w.poll())
            if w.poll() is not None:
                actualy_running_workers.append(w)
                workers_to_start -= 1
            # TODO: check, if the returncode is 0 or fail
        self.running_workers = actualy_running_workers

        workers_to_start = max(0,workers_to_start)
        print("going to start %d workers" % workers_to_start)
        env = os.environ
#        env['DJANGO_SETTINGS_MODULE'] = "mtcepy_site.testsettings"

        for i in range(workers_to_start):
#            subpr = subprocess.Popen("./manage.py evaluation_worker -v 3 --settings mtcepy_site.testsettings".split(),env=env)
            subpr = subprocess.Popen("./manage.py evaluation_worker -v 3".split(),env=env)
            self.running_workers.append(subpr)

