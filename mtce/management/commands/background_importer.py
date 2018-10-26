from django.core.management.base import BaseCommand

from mtce.models import *
import mtce.apps

import time
import os
import shutil

class Command(BaseCommand):

    help = "Whatever you want to print here"

    def handle(self, *args, **options):
        print(args)
        print(options)

        importing_loop()

mtce.apps.update_file_structure = False
base = os.path.join("files","comparisons")

def import_comparison(path):
    print("     importing ", path)
    name = os.path.basename(path)
    src = os.path.join(path, "source.txt")
    ref = os.path.join(path, "reference.txt")
    c = Comparison(name=name,origsourcefile=src,origreferencefile=ref)
    c.save()
    di = create_DataImport(src,"source.txt",c)
    di.save()
    di = create_DataImport(ref,"reference.txt",c)
    di.save()

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

                        print("creating MTSystem",sys)
                    print(cdir)
                    cp = create_Checkpoint(cdir,trans,sys)
                    cp.save()
                    di = create_DataImport(trans,'translation.txt',cp)
                    print("creating Checkpoint",cp)
                    di.save()
        else:
            if dir not in ("source.txt","reference.txt"):
                print("ignoring extra file ",path,dir)



def check_comparison(path):
    for file in os.listdir(path):
        pfile = os.path.join(path, file)
        if file in ("source.txt", "reference.txt"):
            if DataImport.needs_new_import(pfile):
                print("new import:", DataImport.needs_new_import(pfile), pfile)
                import_comparison(path)
                return
            elif DataImport.needs_reimport(pfile):
                print("yes, reimport",pfile)
                DataImport.reimport(pfile, file)
        else:
            print("skipping %s" % file)


def importing_loop():
    while True:
        for dir in os.listdir(base):
            bdir = os.path.join(base, dir)
            if os.path.isdir(bdir):
                print(bdir)
                check_comparison(bdir)
            else:
                print("skipping %s, it is not a dir" % dir)
        print()
        time.sleep(2)
        break
