from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Comparison, Checkpoint, MTSystem


def get_comparisons():
    return Comparison.objects.all() #order_by('name') \
       # .annotate(documents=Count('document')) \
       # .annotate(total_sentences=Count('document__sentence'))
    # tasks_table = TaskTable(tasks)

def index(request):
    """
    The initial dashboard view with a list of tasks
    """
    comparisons = get_comparisons()

    return render(
        request,
        'mtce/index.html',
        {'comparisons': comparisons,
         'active': 'comp'},
    )

def help(request):
    comparisons = get_comparisons()

    return render(
        request,
        'mtce/help.html',
        {'comparisons': comparisons,
         'active': 'help'},
    )

def edit(request):
    comparisons = get_comparisons()
    return render(
        request,
        'mtce/edit.html',
        {'comparisons': comparisons,
         'active': 'edit'},
    )

def comparison_detail(request, comparison_id):


    comp = get_object_or_404(Comparison, pk=comparison_id)

    systems_checkpoints = comp.systems_checkpoints()
    list_source_reference = comp.list_source_reference(beg=0,end=100)
    return render(request,
                  'mtce/comparison_detail.html',
                  {'comparison': comp,
                   'comparisons': get_comparisons(),
                   'active': 'comp',
                   'systems_checkpoints': systems_checkpoints,
                   'list_source_reference': list_source_reference,
                   }
                  )


def system_detail(request, system_id):

    sys = get_object_or_404(MTSystem, pk=system_id)

    comp = sys.comparison
    checkpoints = sys.checkpoints()
    return render(request,
                  'mtce/system_detail.html',
                  {'comparison': comp,
                   'system': sys,
                   'comparisons': get_comparisons(),
                   'active': 'system',
                   'checkpoints': checkpoints,
                   }
                  )
