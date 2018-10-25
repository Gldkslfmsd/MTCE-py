from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Dataset

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def index(request):
    """
    The initial dashboard view with a list of tasks
    """
    datasets = Dataset.objects.all() #order_by('name') \
       # .annotate(documents=Count('document')) \
       # .annotate(total_sentences=Count('document__sentence'))
    # tasks_table = TaskTable(tasks)

    return render(
        request,
        'mtce/index.html',
        {'datasets': datasets},
    )

def dataset_detail(request, dataset_id):
    return index(request)