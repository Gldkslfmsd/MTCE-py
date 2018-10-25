from django.db import models
from django.utils.translation import ugettext as _
import os
import shutil
# Create your models here.



class ModelBase():

    def __str__(self):
        return self.name


    ######################
    # file structure

    upload_to_base = "files"
    upload_to_tmp = os.path.join("files","tmp")
    structure_base = os.path.join("files","comparisons")

    def copy_to(self, origin, new):
        dir = os.path.dirname(new)
        if not os.path.exists(dir):
            os.makedirs(dir)
        shutil.copyfile(origin, new)

    def count_number_of_lines(self, A):
        n = 0
        with open(A,"r") as fA:
            for line in fA:
#                print(line)
                n += 1
#        print(n)
#        print()
        return n

    def correct_number_of_lines(self, A,B):
        nA, nB = self.count_number_of_lines(A), self.count_number_of_lines(B)
        if nA != nB or nA == 0:
            return False
        return True




class Comparison(ModelBase, models.Model):

    name = models.CharField(max_length=200)

    origsourcefile = models.FileField(
        upload_to=ModelBase.upload_to_tmp,
        help_text=_("Text file with one source sentence per line")
    )

    origreferencefile = models.FileField(
        upload_to=ModelBase.upload_to_tmp,
        help_text=_("Text file with one reference sentence per line")
    )

    description = models.TextField(max_length=5000, default="", blank=True, help_text="Optional dataset description")

    def systems_checkpoints(self):
        return ((s,c) for s in self.mtsystem_set.all() for c in s.checkpoint_set.all())

    is_imported = models.BooleanField(default=False)
    is_corrupted = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    #################
    # file structure

    def sourcefile(self):
        return os.path.join(self.base_dir(),"source.txt")

    def referencefile(self):
        return os.path.join(self.base_dir(),"reference.txt")

    def base_dir(self):
        basename = os.path.join(self.structure_base, "comparison_%d" % self.id)
        return basename

    def update_file_structure(self):
        if self.is_checked: return
        self.copy_to(self.origsourcefile.name, self.sourcefile())
        self.copy_to(self.origreferencefile.name, self.referencefile())

        if not self.correct_number_of_lines(self.sourcefile(), self.referencefile()):
            self.is_corrupted = True
        self.is_checked = True
        self.save()


    def delete_file_structure(self):
        shutil.rmtree(self.base_dir())



class MTSystem(ModelBase, models.Model):
    name = models.CharField(max_length=200)
    comparison = models.ForeignKey(Comparison, on_delete=models.CASCADE)

    description = models.TextField(max_length=5000, default="", blank=True, help_text="Optional MTSystem description")

    def checkpoints(self):
        return self.checkpoint_set.all()

    def base_dir(self):
        basename = os.path.join(self.comparison.base_dir(), "mtsystem_%d" % self.id)
        return basename

    def delete_file_structure(self):
        shutil.rmtree(self.base_dir())

    is_imported = models.BooleanField(default=False)

class Checkpoint(ModelBase, models.Model):
    name = models.CharField(max_length=200)
    mtsystem = models.ForeignKey(MTSystem, on_delete=models.CASCADE)

    step = models.IntegerField(default=-1, help_text="MT system trainings steps of this checkpoint. Optional.")
    epoch = models.FloatField(default=-1, help_text="Number of epochs (aka iterations on training data) for this checkpoint. Optional.")
    time = models.IntegerField(default=-1, help_text="Training time in number of seconds needed to obtain this checkpoint. Optional.")


    origtranslationfile = models.FileField(
        upload_to=ModelBase.upload_to_tmp,
        help_text=_("Translation file")
    )

    def comparison(self):
        return self.mtsystem.comparison

    def base_dir(self):
        basename = os.path.join(self.mtsystem.base_dir(), "checkpoint_%d" % self.id)
        return basename

    def translationfile(self):
        return os.path.join(self.base_dir(), "translation.txt")

    def update_file_structure(self):
        if self.is_checked: return
        self.copy_to(self.origtranslationfile.name, self.translationfile())
        if not self.correct_number_of_lines(self.translationfile(), self.mtsystem.comparison.sourcefile()):
            self.is_corrupted = True
        self.is_checked = True
        self.save()

    def delete_file_structure(self):
        shutil.rmtree(self.base_dir())

    is_imported = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)
