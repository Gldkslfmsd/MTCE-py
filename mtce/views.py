from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse
from .models import Comparison, Checkpoint, MTSystem
from .evaluators import METRICS
from .charts import *
from .sentence_listing import get_all_sentences
from .pairwise_diff import *
import random

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

    pass_args = {
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
                   pass_args ,
                  )

def system_index(request, system_id):
    system = get_object_or_404(MTSystem, pk=system_id)
    return corpus_metrics(request, system.comparison.id, system)



def sentences_query(request, comparison_id, orderby, first, diff, dir, system=None, beg=0, end=100):
    comp = get_object_or_404(Comparison, pk=comparison_id)

    sentences = get_all_sentences(comp,system)

    if sentences == []:
        return HttpResponse("")

    if orderby == "document":
        if dir == "desc":
            sentences = sentences[::-1]
    elif orderby == "random":
        random.shuffle(sentences)
    else:
        _, metric = orderby.split(">>>")
        _, cp = first.split(">>>")
        cp = int(cp)
        indeces = [ s.id for s in sentences[0]]
        first_ind = indeces.index(cp)
        if diff != "-":
            _, diff = diff.split(">>>")
            diff = int(diff)
            diff_ind = indeces.index(diff)
            def orderkey(sents):
                return sents[first_ind].orderkey(metric) - sents[diff_ind].orderkey(metric)
        else:
            def orderkey(sents):
                return sents[first_ind].orderkey(metric)

        if dir == "desc":
            reverse = True
        else:
            reverse = False
        sentences = sorted(sentences, key=orderkey, reverse=reverse)

    sentences = sentences[beg:end]
    pass_args = {
                   'active':"sentences",  # for top menu
                   'comparison': comp,
                   'system': system,
                   'sentences': sentences,
                   'first_sentences': sentences[0],
                   'checkpoint_names': [ s.name for s in sentences[0] if s.has_metrics ],
                   'metrics': sentences[0][-1].metrics,
                   }
    return render(request,
                  'mtce/sentences_tables.html',
                   pass_args,
                  )



def sentences(request, comparison_id, system=None):

    comp = get_object_or_404(Comparison, pk=comparison_id)

    sentences = get_all_sentences(comp,system)[:200]
    pass_args = {
                   'active':"sentences",  # for top menu
                   'comparison': comp,
                   'system': system,
                   'sentences': sentences,
                   'first_sentences': sentences[0],
                   'checkpoint_names': [ s.name for s in sentences[0] if s.has_metrics ],
                   'metrics': sentences[0][-1].metrics,
                   }
    return render(request,
                  'mtce/sentences.html',
                   pass_args,
                  )

def system_sentences(request, system_id):
    system = get_object_or_404(MTSystem, pk=system_id)
    return sentences(request, system.comparison.id, system)



def pairwise_index_args(comp, system):
    metrics = METRICS
    systems_checkpoints = comp.systems_checkpoints()
    if system is not None:
        systems_checkpoints = [(s,ch) for s,ch in systems_checkpoints if s == system]

    systems_checkpoints_metricvalues = [ (s,ch,[ round(ch.get_metric_value(m),2) for m in metrics]) for s,ch in systems_checkpoints ]

    pass_args = {
                   'active':"pairwise",  # for menu
                   'comparison': comp,
                   'systems_checkpoints_metricvalues': systems_checkpoints_metricvalues,
                   'metrics':metrics,
#                   'metric_bar_charts': [ MetricBarChart(metric,[(a,b,c[i]) for a,b,c in systems_checkpoints_metricvalues]) \
#                                                         for i,metric in enumerate(metrics) ]+[RadarChart()],
                   'system': system,
                   }
    return pass_args

def pairwise_index(request, comparison_id, system=None):
    comp = get_object_or_404(Comparison, pk=comparison_id)
    pass_args = pairwise_index_args(comp, system)
    return render(request,
                  'mtce/pairwise_index.html',
                   pass_args ,
                  )



def pairwise_diff(request, comparison_id, system=None):
    comp = get_object_or_404(Comparison, pk=comparison_id)
    checkpoint_A, checkpoint_B = map(int,request.POST.getlist("choice[]"))
    print(checkpoint_B, checkpoint_A)
    A = get_object_or_404(Checkpoint, pk=checkpoint_A)
    B = get_object_or_404(Checkpoint, pk=checkpoint_B)
    A.nicename = A.nice_name()
    B.nicename = B.nice_name()
    print(checkpoint_A, A)
    print(checkpoint_B, B)
    pass_args = pairwise_index_args(comp, system)
    pa = {
        'sent_level_charts':sentence_level_charts(A, B),
        'bootstrap_charts': bootraps(A, B),
        'checkpoint_A': A,
        'checkpoint_B': B,
    }
    pass_args.update(pa)
    return render(request,
                  'mtce/pairwise_diff.html',
                  pass_args
                  )

