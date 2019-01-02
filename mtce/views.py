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

    obj_dict = {'comparison': comp,
                   'systems_checkpoints_metricvalues': systems_checkpoints_metricvalues,
                   'metrics':metrics,
                   'metric_bar_charts': [ MetricBarChart(metric,[(a,b,c[i]) for a,b,c in systems_checkpoints_metricvalues]) \
                                                         for i,metric in enumerate(metrics) ],
                   }

    d = get_senteces_to_show(comp)
    obj_dict.update(d)
    return render(request,
                  'mtce/comparison_overview.html',
                   obj_dict,
                  )


def system_overview(request, system_id):

    sys = get_object_or_404(MTSystem, pk=system_id)

    comp = sys.comparison
    checkpoints = sys.checkpoints()
#    print([ (ch,[round(ch.get_metric_value(m),2) for m in METRICS]) for ch in checkpoints ])
    metrics = METRICS
    checkpoints_metricvalues = [ (ch,[ round(ch.get_metric_value(m),2) for m in metrics]) for ch in checkpoints ]

    obj_dict = {'comparison': comp,
                   'system': sys,
                   'comparisons': get_comparisons(),
                   'checkpoints': checkpoints,
                   'metrics':METRICS,
                   'checkpoints_metricvalues':[ (ch,[round(ch.get_metric_value(m),2) for m in METRICS]) for ch in checkpoints ],
                   'metric_bar_charts': [ MetricBarChart(metric,[(sys, b,c[i]) for b,c in checkpoints_metricvalues]) \
                                                         for i,metric in enumerate(metrics) ],
                   }

    d = get_senteces_to_show(comp)
    obj_dict.update(d)
    return render(request,
                  'mtce/system_overview.html',
                  obj_dict
                  )

class Sentence:
    def __init__(self,id,name,text,show):
        self.id = id
        self.text = text
        self.name = name
        self.show = show
def get_senteces_to_show(comp, start=0, end=10):

    sentences = [ [Sentence("src","source",src,True), Sentence("ref","reference",ref,True)] for src, ref in zip(
        comp.browse_sentences("source",start,end), comp.browse_sentences("reference",start,end)) ]
    for i,(sys,cp) in enumerate(comp.systems_checkpoints()):
        name = "%s / %s" % (sys.name,cp.name)
        for sent,cpsent in zip(sentences, cp.browse_sentences("translation",start,end)):
            sent.append(Sentence(cp.id,name,cpsent,i<2))

    return  {
            "sentences": sentences,
            "first_sentences": sentences[0],
             "systems_checkpoints_sentences":[(s,ch,ch.browse_sentences("translation",start,end)) for s,ch in comp.systems_checkpoints() ]
           }

def show_sentences(request, comparison_id, start=0, end=100):
    comp = get_object_or_404(Comparison, pk=comparison_id)

    print("tady")
    return render(request,
                  "mtce/show_sentences.html",

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

