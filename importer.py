

from django.conf import settings
from mtce.models import *

settings.configure()
c = Checkpoint.objects.get(pk=1)

print(c)