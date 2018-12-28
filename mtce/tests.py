from django.test import TestCase
from django import db
# Create your tests here.

from .models import *
from .management.commands.background_importer import *

import os

def copytree(src, dst, symlinks=False, ignore=None):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

base = os.path.join("files","tmp")

class ComparisonTests(TestCase):

    def test_wrong_number_of_lines(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)

        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10)+"\n", file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")

        c.save()
        self.assertIs(c.is_corrupted,True)


    def test_correct_number_of_lines(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        self.assertIs(c.is_corrupted,False)

    def test_empty_files(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,True)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="\n")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="\n")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,False)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="\n")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,False)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n\n", file=f)
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["sd","sds"]), file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        # two lines against two lines
        self.assertIs(c.is_corrupted,True)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("", file=f, end="")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("", file=f, end="")

        c = Comparison(origsourcefile=A,origreferencefile=B,name="test_comparison")
        c.save()
        # two empty files
        self.assertIs(c.is_corrupted,True)

class ComparisonCheckpointTests(TestCase):

    def test_correct_number_of_lines(self):
        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sdfsd\nsdfsd\n", file=f, end="")

        c = Comparison(origsourcefile=A,origreferencefile=A,name="sdfs")
        c.save()
        # two empty files
        self.assertIs(c.is_corrupted,False)

        mt = MTSystem(name="sdfsds",comparison=c)
        mt.save()

        cp = Checkpoint(name="DFSDFS",mtsystem=mt,origtranslationfile=B)
        cp.save()
        self.assertIs(c.is_corrupted,False)

class DataImportTests(TestCase):

    def test_comparison_needs_import(self):
        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        c = Comparison(name="DFS",origsourcefile=A,origreferencefile=A)
        c.save()
        di = create_DataImport(A,"source.txt",c)
        di.save()

        self.assertIs(DataImport.needs_new_import(A),False)
        self.assertIs(DataImport.needs_reimport(A),False)


        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        self.assertIs(DataImport.needs_reimport(A),True)

    def test_checkpoint_needs_import(self):
        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        c = Comparison(name="DFS",origsourcefile=A,origreferencefile=A)
        c.save()
        di = create_DataImport(A,"source.txt",c)
        di.save()

        self.assertIs(DataImport.needs_new_import(A),False)
        self.assertIs(DataImport.needs_reimport(A),False)


        A = os.path.join(base,"test_x")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")

        self.assertIs(DataImport.needs_new_import(A),True)
        sys = MTSystem(name="SDFSDFS",comparison=c)
        sys.save()

        chp = create_Checkpoint("sfs test_comparison d",A,sys)
        chp.save()
        dc = create_DataImport(A,"translation.txt",chp)
        dc.save()

        self.assertIs(DataImport.needs_new_import(A),False)
        self.assertIs(DataImport.needs_reimport(A),False)

        A = os.path.join(base,"test_x")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        self.assertIs(DataImport.needs_reimport(A),True)

    def test_imports(self):
        copytree("files/test/test_comparison","files/comparisons/test_comparison")
        importing_loop_iteration()

        cp = Checkpoint.objects.get(name='test_checkpoint')
        self.assertEqual(cp.name,'test_checkpoint')
        self.assertEqual(cp.get_translation(),open('files/test/test_comparison/test_system/test_checkpoint/translation.txt').read())

        os.remove(cp.translationfile())
        shutil.copy("files/test/test_comparison/source.txt",cp.translationfile())


        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        importing_loop_iteration()

        cp = Checkpoint.objects.get(name='test_checkpoint')
        self.assertEqual(cp.name,'test_checkpoint')
        self.assertNotEqual(cp.get_translation(),open('files/test/test_comparison/test_system/test_checkpoint/translation.txt').read())
        self.assertEqual(cp.get_translation(),open("files/test_comparisons/test_comparison/source.txt").read())

        c = Comparison.objects.get(name="test_comparison")

        with open(c.sourcefile(),"w") as f:
            f.write("test source\n"*10)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        self.assertEquals(DataImport.needs_reimport(c.sourcefile()),True)
        importing_loop_iteration()
        self.assertEquals(DataImport.needs_reimport(c.sourcefile()),False)




from .evaluators import BLEU, BLEU_subprocess
import subprocess
import os
import sacrebleu
from django.conf import settings

#from django_concurrent_tests.helpers import call_concurrently

class TestEvaluator(TestCase):

    marian_wmt18 = "files/test/marian.wmt18.en-de"
    reference_wmt18 = os.path.join(os.path.expanduser("~"),".sacrebleu/wmt18/en-de.de")
    source_wmt18 = os.path.join(os.path.expanduser("~"),".sacrebleu/wmt18/en-de.en")

    @staticmethod
    def prepare_marian_test():
        '''downloads WMT18 en-de src and reference, and Marian's submission from matrix.statmt.org,
         to files/test'''

        import sacrebleu as scb
        scb.download_test_set("wmt18","en-de")

        marian_wmt18 = "http://matrix.statmt.org/data/20180522045237_U-1012_S-3525_T-1881_test2018.en.output.r2l.sgm?1526964802"
        from urllib.request import urlopen
        r = urlopen(marian_wmt18)
        with open("files/test/marian.wmt18.en-de.sgm","w") as f:
            f.write(r.read().decode("utf-8"))
        sacrebleu.process_to_text("files/test/marian.wmt18.en-de.sgm","files/test/marian.wmt18.en-de")


    def test_sacrebleu_calls(self):
        """BLEU computed as with a script versus library is the same now"""

        if not os.path.exists(self.marian_wmt18):
            self.prepare_marian_test()

        ref = self.reference_wmt18
        tr = self.marian_wmt18
        sb = BLEU_subprocess().eval(tr,ref)
        b = round(BLEU().eval(tr,ref),2)
        self.assertEquals(sb,b)

    def test_evaluation(self):
        c = Comparison(name="en-de WMT18",origsourcefile=self.source_wmt18,origreferencefile=self.reference_wmt18)
        c.save()
        s = MTSystem(name="marian",comparison=c)
        s.save()
        mts = MTSystem.objects.get(name="marian")
        self.assertEqual(s,mts)
        ch = create_Checkpoint("checkpoint-1",self.marian_wmt18,mts)
        ch.save()

        print("######")
        for c in Comparison.objects.all():
            print(c)
        for s in MTSystem.objects.all():
            print(s,s.checkpoint_set.all())
        for ch in Checkpoint.objects.all():
            print(ch,ch.mtsystem)
        print("###### EvalJobs:")
        for ej in EvalJob.objects.all():
            print(ej)
        print("#########")
        j = EvalJob.acquire_job_or_none()
        self.assertIsNotNone(j)
        print("###### EvalJobs:")
        for ej in EvalJob.objects.all():
            print(ej)
        print("#########")

        em = EvaluationManager(1)
        em.evaluation_manager_iteration()

        time.sleep(20)
        print("-------------------- all jobs:", settings.DATABASES)
        for s in EvalJob.objects.all():
            print(s)
        print("----")



    def test_concurrent_db_access(self):

        def racey_function(arg):
            print("abc")
            return "SDFSFDSFS"
            c = Comparison(name="concurrent_test%d" % arg,origsourcefile=self.source_wmt18,origreferencefile=self.reference_wmt18)
            c.save()
            return True

        def is_success(result):
            return result is True and not isinstance(result, Exception)


        results = call_concurrently(1, racey_function, first_arg=1)
        time.sleep(1)
        print(results)
        # results contains the return value from each call
        successes = list(filter(is_success, results))












