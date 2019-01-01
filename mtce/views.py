from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Comparison, Checkpoint, MTSystem
from .evaluators import METRICS

from .charts import *

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
        {'comparisons': comparisons
         },
    )


def comparison_overview(request, comparison_id):


    comp = get_object_or_404(Comparison, pk=comparison_id)

    metrics = METRICS
    systems_checkpoints = comp.systems_checkpoints()
    systems_checkpoints_metricvalues = [ (s,ch,[ round(ch.get_metric_value(m),2) for m in metrics]) for s,ch in systems_checkpoints ]
    return render(request,
                  'mtce/comparison_overview.html',
                  {'comparison': comp,
                   'systems_checkpoints_metricvalues': systems_checkpoints_metricvalues,
                   'metrics':metrics,
                   'metric_bar_charts': [ MetricBarChart(metric,[(a,b,c[i]) for a,b,c in systems_checkpoints_metricvalues]) \
                                                         for i,metric in enumerate(metrics) ],
#                   'line_chart': RadarChart(),
                   }
                  )


def system_overview(request, system_id):

    sys = get_object_or_404(MTSystem, pk=system_id)

    comp = sys.comparison
    checkpoints = sys.checkpoints()
#    print([ (ch,[round(ch.get_metric_value(m),2) for m in METRICS]) for ch in checkpoints ])
    metrics = METRICS
    checkpoints_metricvalues = [ (ch,[ round(ch.get_metric_value(m),2) for m in metrics]) for ch in checkpoints ]
    return render(request,
                  'mtce/system_overview.html',
                  {'comparison': comp,
                   'system': sys,
                   'comparisons': get_comparisons(),
                   'checkpoints': checkpoints,
                   'metrics':METRICS,
                   'checkpoints_metricvalues':[ (ch,[round(ch.get_metric_value(m),2) for m in METRICS]) for ch in checkpoints ],
                   'metric_bar_charts': [ MetricBarChart(metric,[(sys, b,c[i]) for b,c in checkpoints_metricvalues]) \
                                                         for i,metric in enumerate(metrics) ],
                   }
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

