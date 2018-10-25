from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Dataset)
admin.site.register(MTSystem)
admin.site.register(Checkpoint)