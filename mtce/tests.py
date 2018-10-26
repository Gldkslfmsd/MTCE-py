from django.test import TestCase

# Create your tests here.

from .models import *

import os

base = os.path.join("files","tmp")

class ComparisonTests(TestCase):

    def test_wrong_number_of_lines(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)

        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10)+"\n", file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")

        c.save()
        self.assertIs(c.is_corrupted,True)


    def test_correct_number_of_lines(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["xdfs sdf s fd s fs dd s"]*10), file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
        c.save()
        self.assertIs(c.is_corrupted,False)

    def test_empty_files(self):

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,True)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="\n")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="\n")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,False)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n", file=f,end="\n")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("sd\nsds", file=f,end="")
        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
        c.save()
        # this is 1 line against 2 lines
        self.assertIs(c.is_corrupted,False)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("\n\n", file=f)
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("\n".join(["sd","sds"]), file=f)

        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
        c.save()
        # two lines against two lines
        self.assertIs(c.is_corrupted,True)

        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("", file=f, end="")
        B = os.path.join(base,"test_b")
        with open(B, "w") as f:
            print("", file=f, end="")

        c = Comparison(origsourcefile=A,origreferencefile=B,name="sdfs")
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

    def test_needs_import(self):
        A = os.path.join(base,"test_a")
        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        c = Comparison(name="DFS",origsourcefile=A,origreferencefile=A)
        c.save()
        di = create_DataImport(A,"source.txt",c)
        di.save()

        self.assertIs(DataImport.needs_new_import(A),False)
        self.assertIs(DataImport.needs_reimport(A),False)
        self.assertIs(DataImport.needs_reimport(A),False)


        with open(A, "w") as f:
            print("abc\nsdfd\n", file=f, end="")
        self.assertIs(DataImport.needs_reimport(A),True)


