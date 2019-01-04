import sacrebleu
import subprocess
import numpy as np

from .bootstrap import get_masks, bootstrap_corpus_bleu

class Evaluator:


    BOOTSTRAP_SAMPLES = 1000
    BOOTSTRAP_SIZES = 300

    def open_files_mask(self, trans, ref, mask):
        with open(trans,"r") as trans:
            t = trans.readlines()
        with open(ref,"r") as ref:
            r = ref.readlines()
        if mask is not None:
            t = np.array(t)[mask]
            r = np.array(r)[mask]
        return t,r

    def eval(self,translation,reference,mask=None,bootstrap_samples=None,bootstrap_sizes=None):
        """
        :param translation:  filename
        :param reference:  filename
        :param bootstrap_samples: overrides the default self.BOOTSTRAP_SAMPLES
        :param bootstrap_sizes: as above
        :param mask: If None, the whole testset will be evaluated. Otherwise, the evaluation will be performed only
        on a subsample of sentences determined by the mask. The mask is an np.array of sentence indeces.
        :return: a dict of floats or dicts of following shape:
            { "metric_name": 0.23,  # only a corpus metric is computed (on the subsample determined by the eventual mask)

              "metric_name2: {  # the metric for the whole corpus, all sentences or bootstrap samples (all optional)
                            "corpus": 32.45,
                            "sentences": [0.22, 43.34, 43.43, ...],
                            "bootstrap": [0.22, 43.34, 43.43, ...],
                             },
              ...
             }
        """
        raise NotImplementedError()

def get_corpus_metric(result,metric):
    assert metric in result
    res = result[metric]
    if isinstance(res,dict):
        return res["corpus"]
    return res

class BLEUEvaluator(Evaluator):

    LOWERCASE = False

    def eval(self,trans,ref,mask=None, **kw):
        """works for only one reference"""
        print(trans)
        print(ref)
        t,r = self.open_files_mask(trans, ref, mask)
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return {(BLEU if not self.LOWERCASE else BLEU_LOWER):bleu.score}


class BLEU_subprocess(Evaluator):
    """For debuggin and testing purposes only. Runs sacrebleu in subprocess, which should give the same results
    as runned as a library.
    """

    def eval(self,trans,ref,mask=None, **kw):
        output = subprocess.check_output(["sacrebleu",ref,"-i",trans,"-b"]).decode('utf-8')
        return {BLEU:float(output)}

class BLEU_lc(BLEUEvaluator):
    LOWERCASE = True



class SacreBleu(BLEUEvaluator):

    """Runs sacrebleu BLEU as a library and returns more metrics."""

    def eval(self,trans,ref,mask=None, **kw):
        """works for only one reference"""
        t,r = self.open_files_mask(trans, ref, mask)
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return {BLEU:bleu.score,
                BREVITY_PENALTY:bleu.bp}

class SentenceBleu(BLEUEvaluator):

    def eval(self, trans, ref, mask=None, **kw):
        trans,ref = self.open_files_mask(trans, ref, mask)
        sentence_bleus = [ sacrebleu.sentence_bleu(t,r) for t,r in zip(trans,ref) ]
        return {BLEU: {"sentences": sentence_bleus}}


class BootstrapSacreBleu(BLEUEvaluator):

    def eval(self, trans, ref, mask=None, bootstrap_samples=None,bootstrap_sizes=None):
        if bootstrap_samples is None:
            bootstrap_samples = self.BOOTSTRAP_SAMPLES
        if bootstrap_sizes is None:
            bootstrap_sizes = self.BOOTSTRAP_SIZES
        t,r = self.open_files_mask(trans, ref, mask)
        bleus = bootstrap_corpus_bleu(t,[r],get_masks(trans,bootstrap_samples,bootstrap_sizes))
        return {BLEU: {"bootstrap": bleus }}

# the metrics names showed in front-end and stored to db
BLEU = "BLEU"
BREVITY_PENALTY = "brevity penalty"
BLEU_LOWER = "BLEU lowercased"

# list of corpus metrics to show in front-end, in this order
METRICS = [ BLEU,
            BLEU_LOWER,
            BREVITY_PENALTY,
]

EVALUATORS = [
    BLEU_lc(),
    SacreBleu(),
    BootstrapSacreBleu(),
    SentenceBleu(),
]

#METRICS = list(set(x for e in EVALUATORS.keys() for x in e.split()))



#BOOTSTRAP_EVALUATORS = {
#    ("BLEU",1000,100): SacreBleu(),
#}


# default values for not available metrics

from collections import defaultdict
metric_NA = defaultdict(lambda: float("nan"))
metric_NA["BLEU"] = -1

# ranges to plot
METRICS_RANGES = defaultdict(lambda: (0, 100))
METRICS_RANGES[BREVITY_PENALTY] = (0.0, 1.0)
