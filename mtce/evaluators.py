

import sacrebleu
import subprocess
import numpy as np

from .bootstrap import get_masks, bootstrap_corpus_bleu

class Evaluation:

    def open_files_mask(self, trans, ref, mask):
        with open(trans,"r") as trans:
            t = trans.readlines()
        with open(ref,"r") as ref:
            r = ref.readlines()
        if mask is not None:
            t = np.array(t)[mask]
            r = np.array(r)[mask]
        return t,r

    def eval(self,translation,reference,mask=None):
        raise NotImplementedError()

class BLEU(Evaluation):

    LOWERCASE = False

    def eval(self,trans,ref,mask=None):
        """works for only one reference"""
        print(trans)
        print(ref)
        t,r = self.open_files_mask(trans, ref, mask)
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return (bleu.score,)


class BLEU_subprocess(Evaluation):

    def eval(self,trans,ref,mask=None):
        output = subprocess.check_output(["sacrebleu",ref,"-i",trans,"-b"]).decode('utf-8')
        return (float(output),)

class BLEU_lc(BLEU):
    LOWERCASE = True

class SacreBleu(BLEU):

    def eval(self,trans,ref,mask=None):
        """works for only one reference"""
        t,r = self.open_files_mask(trans, ref, mask)
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return bleu.score, bleu.bp

class BootstrapSacreBleu(BLEU):

    def eval(self, trans, ref, mask=None):
        #print(trans)
        #print(ref)
        t,r = self.open_files_mask(trans, ref, mask)
        #print(t)
        #print("---------")
        #print(r)
        bleus = bootstrap_corpus_bleu(t,[r],get_masks(trans,1000,100))
        return (bleus,)


EVALUATORS = {
#    "BLEU": BLEU(),
    "BLEU_lowercased": BLEU_lc(),
    "BLEU brevity_penalty": SacreBleu(),
    "BootstrapBLEU": BootstrapSacreBleu(),
}


METRICS = ["BLEU",
           "brevity_penalty",
           "BLEU_lowercased",
           ]

from collections import defaultdict
metric_NA = defaultdict(lambda: float("nan"))
metric_NA["BLEU"] = -1
