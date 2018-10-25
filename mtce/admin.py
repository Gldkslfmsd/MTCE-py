from django.contrib import admin

# Register your models here.

from .models import *

from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

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

admin.site.register(Comparison, ComparisonAdmin)

#admin.site.register(MTSystem, MTSystemAdmin)
#admin.site.register(Checkpoint)