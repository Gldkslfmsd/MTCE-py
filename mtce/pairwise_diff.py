from .models import *
from .evaluators import METRICS


from .charts import SentLevelDiffChart

import numpy as np


def sentence_level_diffs(A, B):

    a = A.get_sentence_evaluations_dict()
    b = B.get_sentence_evaluations_dict()
    print(a, b)


    charts = []
    for metric in a.keys():
        assert metric in b
        diff = np.array(a[metric].float_values()) - \
            np.array(b[metric].float_values())
        diffs = sorted(diff)
        ch = SentLevelDiffChart(diffs, metric, A.nice_name(), B.nice_name())
        charts.append(ch)

    return charts
