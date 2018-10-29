
import os

import sacrebleu
import subprocess

class Evaluation:
    def eval(self,translation,reference):
        raise NotImplementedError()

class BLEU(Evaluation):

    def eval(self,trans,ref):
        """works for only one reference"""
        with open(trans,"r") as trans:
            t = trans.readlines()
        with open(ref,"r") as ref:
            r = ref.readlines()
        bleu = sacrebleu.corpus_bleu(t,[r])
        return bleu.score


class BLEU_subprocess(Evaluation):

    def eval(self,trans,ref):
        output = subprocess.check_output(["sacrebleu",ref,"-i",trans,"-b"]).decode('utf-8')
        return float(output)
