from django.contrib import admin

# Register your models here.

from .models import *

from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

# this demo helped me a lot: https://www.bedjango.com/blog/how-use-django-nested-admin/

class CheckpointStackedInline(NestedStackedInline):
    model = Checkpoint
    extra = 1

class MTSystemTabularInline(NestedTabularInline):
    model = MTSystem
    extra = 1
    inlines = [CheckpointStackedInline, ]

class ComparisonAdmin(NestedModelAdmin):
    list_display = ('name','description')
    inlines = [MTSystemTabularInline,] # CheckpointStackedInline]
    search_fields = ['name','description']





@receiver(post_save, sender=Comparison)
@receiver(post_save, sender=Checkpoint)
def post_save_receiver(senderclass=None, signal=None, instance=None, created=False, update_fields=None, raw=False, using='default', **kwargs):
    instance.update_file_structure()


@receiver(pre_delete, sender=Comparison)
@receiver(pre_delete, sender=Checkpoint)
@receiver(pre_delete, sender=MTSystem)
def pre_delete_receiver(senderclass=None, signal=None, instance=None, created=False, update_fields=None, raw=False, using='default', **kwargs):
    instance.delete_file_structure()


admin.site.register(Comparison, ComparisonAdmin)

#admin.site.register(MTSystem, MTSystemAdmin)
#admin.site.register(Checkpoint)



