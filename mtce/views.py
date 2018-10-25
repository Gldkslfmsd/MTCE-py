from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Comparison

def index(request):
    return HttpResponse("Hello, world. You're at the index.")


def index(request):
    """
    The initial dashboard view with a list of tasks
    """
    comparisons = Comparison.objects.all() #order_by('name') \
       # .annotate(documents=Count('document')) \
       # .annotate(total_sentences=Count('document__sentence'))
    # tasks_table = TaskTable(tasks)

    return render(
        request,
        'mtce/index.html',
        {'comparisons': comparisons},
    )

def comparison_detail(request, comparison_id):

    comp = get_object_or_404(Comparison, pk=comparison_id)

    print(comp)

    return render(request,
                  'mtce/comparison_detail.html',
                  {'comparison': comp}
                  )