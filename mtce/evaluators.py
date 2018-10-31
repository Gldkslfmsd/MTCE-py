

import sacrebleu
import subprocess

class Evaluation:
    def eval(self,translation,reference):
        raise NotImplementedError()

class BLEU(Evaluation):

    LOWERCASE = False

    def eval(self,trans,ref):
        """works for only one reference"""
        with open(trans,"r") as trans:
            t = trans.readlines()
        with open(ref,"r") as ref:
            r = ref.readlines()
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return (bleu.score,)


class BLEU_subprocess(Evaluation):

    def eval(self,trans,ref):
        output = subprocess.check_output(["sacrebleu",ref,"-i",trans,"-b"]).decode('utf-8')
        return (float(output),)

class BLEU_lc(BLEU):
    LOWERCASE = True

class SacreBleu(BLEU):

    def eval(self,trans,ref):
        """works for only one reference"""
        with open(trans,"r") as trans:
            t = trans.readlines()
        with open(ref,"r") as ref:
            r = ref.readlines()
        bleu = sacrebleu.corpus_bleu(t,[r], lowercase=self.LOWERCASE)
        return bleu.score, bleu.bp

EVALUATORS = {
#    "BLEU": BLEU(),
    "BLEU_lowercased": BLEU_lc(),
    "BLEU brevity_penalty": SacreBleu(),
}
