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
        {'comparisons': comparisons,
         'active': 'index',
         },
    )



def corpus_metrics(request, comparison_id, system=None):

    comp = get_object_or_404(Comparison, pk=comparison_id)

    metrics = METRICS
    systems_checkpoints = comp.systems_checkpoints()
    if system is not None:
        systems_checkpoints = [(s,ch) for s,ch in systems_checkpoints if s == system]

    systems_checkpoints_metricvalues = [ (s,ch,[ round(ch.get_metric_value(m),2) for m in metrics]) for s,ch in systems_checkpoints ]

    obj_dict = {
                   'active':"corpus_metrics",  # for menu
                   'comparison': comp,
                   'systems_checkpoints_metricvalues': systems_checkpoints_metricvalues,
                   'metrics':metrics,
                   'metric_bar_charts': [ MetricBarChart(metric,[(a,b,c[i]) for a,b,c in systems_checkpoints_metricvalues]) \
                                                         for i,metric in enumerate(metrics) ],
                   'system': system,
                   }

    return render(request,
                  'mtce/corpus_metrics.html',
                   obj_dict,
                  )

def system_index(request, system_id):
    system = get_object_or_404(MTSystem, pk=system_id)
    return corpus_metrics(request, system.comparison.id, system)

def sentences(request, comparison_id, system=None):

    comp = get_object_or_404(Comparison, pk=comparison_id)

    obj_dict = {
                   'active':"sentences",  # for top menu
                   'comparison': comp,
                   'system': system,
                   }

    d = get_senteces_to_show(comp, system)
    obj_dict.update(d)
    return render(request,
                  'mtce/sentences.html',
                   obj_dict,
                  )

def system_sentences(request, system_id):
    system = get_object_or_404(MTSystem, pk=system_id)
    return sentences(request, system.comparison.id, system)























class Sentence:
    def __init__(self,id,name,text,show):
        self.id = id
        self.text = text
        self.name = name
        self.show = show
def get_senteces_to_show(comp, system=None, start=0, end=10):

    sentences = [ [Sentence("src","source",src,True), Sentence("ref","reference",ref,True)] for src, ref in zip(
        comp.browse_sentences("source",start,end), comp.browse_sentences("reference",start,end)) ]
    if system is None:
        systems_checkpoints = comp.systems_checkpoints()
    else:
        systems_checkpoints = [ (s,ch) for s,ch in comp.systems_checkpoints() if s==system]
    for i,(sys,cp) in enumerate(systems_checkpoints):
        if system is not None and sys != system: continue
        name = "%s / %s" % (sys.name,cp.name)
        for sent,cpsent in zip(sentences, cp.browse_sentences("translation",start,end)):
            sent.append(Sentence(cp.id,name,cpsent,i<2))


    return  {
            "sentences": sentences,
            "first_sentences": sentences[0],
             "systems_checkpoints_sentences":[(s,ch,ch.browse_sentences("translation",start,end)) for s,ch in systems_checkpoints]
           }

