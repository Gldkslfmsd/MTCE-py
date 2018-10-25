from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class StrName():

    def __str__(self):
        return self.name

class Comparison(StrName, models.Model):

    name = models.CharField(max_length=200)

    sourcefile = models.FileField(
        upload_to='files/dataset/sources',
        help_text=_("Text file with one source sentence per line")
    )

    referencefile = models.FileField(
        upload_to='files/dataset/references',
        help_text=_("Text file with one reference sentence per line")
    )

    description = models.TextField(max_length=5000, default="", blank=True, help_text="Optional dataset description")


class MTSystem(StrName, models.Model):
    name = models.CharField(max_length=200)
    comparison = models.ForeignKey(Comparison, on_delete=models.CASCADE)

    description = models.TextField(max_length=5000, default="", blank=True, help_text="Optional MTSystem description")

class Checkpoint(StrName, models.Model):
    name = models.CharField(max_length=200)
    mtsystem = models.ForeignKey(MTSystem, on_delete=models.CASCADE)

    step = models.IntegerField(default=-1, help_text="MT system trainings steps of this checkpoint. Optional.")
    epoch = models.FloatField(default=-1, help_text="Number of epochs (aka iterations on training data) for this checkpoint. Optional.")
    time = models.IntegerField(default=-1, help_text="Training time in number of seconds needed to obtain this checkpoint. Optional.")


    translationfile = models.FileField(
        upload_to='files/translations',
        help_text=_("Translation file")
    )

