from django.test import TestCase

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
        importing_loop(infinite=False)

        cp = Checkpoint.objects.get(name='test_checkpoint')
        self.assertEqual(cp.name,'test_checkpoint')
        self.assertEqual(cp.get_translation(),open('files/test/test_comparison/test_system/test_checkpoint/translation.txt').read())

        os.remove(cp.translationfile())
        shutil.copy("files/test/test_comparison/source.txt",cp.translationfile())


        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        importing_loop(infinite=False)

        cp = Checkpoint.objects.get(name='test_checkpoint')
        self.assertEqual(cp.name,'test_checkpoint')
        self.assertNotEqual(cp.get_translation(),open('files/test/test_comparison/test_system/test_checkpoint/translation.txt').read())
        self.assertEqual(cp.get_translation(),open("files/test_comparisons/test_comparison/source.txt").read())

        c = Comparison.objects.get(name="test_comparison")

        with open(c.sourcefile(),"w") as f:
            f.write("test source\n"*10)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        self.assertEquals(DataImport.needs_reimport(c.sourcefile()),True)
        importing_loop(infinite=False)
        self.assertEquals(DataImport.needs_reimport(c.sourcefile()),False)





