from .models import *
from .evaluators import METRICS


from .charts import SentLevelDiffChart, BootstrapChart

import numpy as np


def sentence_level_charts(A, B):

    a = A.get_sentence_evaluations_dict()
    b = B.get_sentence_evaluations_dict()
    print(a, b)


    charts = []
    for metric in a.keys():
        assert metric in b
        diff = a[metric] - b[metric]
        diffs = sorted(diff)
        ch = SentLevelDiffChart(diffs, metric, A.nice_name(), B.nice_name())
        charts.append(ch)

    return charts



def bootraps(A,B):
    a = A.get_bootstrap_values_dict()
    b = B.get_bootstrap_values_dict()

    charts = []
    for metric in a.keys():
        assert metric in b
        ch = BootstrapChart(metric, a[metric], b[metric], A.nice_name(), B.nice_name())
        charts.append(ch)
    return charts
