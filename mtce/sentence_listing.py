from .models import *
from .evaluators import METRICS

class Sentence:
    """This is a class th"""
    def __init__(self,id,name,text,show, metrics_values=None, metrics=None):
        """
        :param id: sentence HTML id attribute suffix. It should be unique within one page.
        :param text: string
        :param name: the tag to display in table (either "source", "reference" or "MTSystem_name / checkpoint")
        :param show: If True, the sentence is by default visible on front-end."""
        self.id = id
        self.text = text
        self.name = name
        self.show = show

        if metrics_values is None:
            metrics_values = []
        self.metrics_values = metrics_values
        if metrics is None:
            metrics = []
        self.metrics = metrics
        self.has_metrics = metrics_values != []

    def add_metric_value(self, metric, value):
        value = "%2.2f" % value
        self.metrics_values.append(value)
        if metric not in self.metrics:
            self.metrics.append(metric)
        self.has_metrics = True




def get_translation_sentences(checkpoint, show):
    name = "%s:%s" % (checkpoint.mtsystem.name, checkpoint.name)
    sents = [ Sentence(checkpoint.id, name, text, show) for text in checkpoint.get_plain_sentences("translation") ]
    sent_ev_dict = { ev.evaluation.metric:ev for ev in checkpoint.get_sentence_evaluations()}
    for m in METRICS:
        if m not in sent_ev_dict: continue
        # convert list formatted as a list to list of floats
        # TODO: consider more effective way of storing list of floats in DB
        values = eval(sent_ev_dict[m].values)
        for sent, v in zip(sents, values):
            sent.add_metric_value(m,v)
    return sents

def get_nontranslation_sentences(id,name, texts, show):
    return [Sentence(id, name, t, show) for t in texts ]





def get_all_sentences(comp, system=None):

    # src and ref
    sentences = [get_nontranslation_sentences("src","source",comp.get_plain_sentences("source"),True),
                get_nontranslation_sentences("ref","reference",comp.get_plain_sentences("reference"),True)]

    if system is None:
        systems_checkpoints = comp.systems_checkpoints()
    else:
        systems_checkpoints = [ (s,ch) for s,ch in comp.systems_checkpoints() if s==system]

    # add the translation, together with metrics
    for i,(sys,cp) in enumerate(systems_checkpoints):
        s = get_translation_sentences(cp,i<2)
        sentences.append(s)

    # Transpose. Now it has a shape [[src, ref, checkpoint1, checkpoint2...], [src, ref, ...]]
    sentences = list(zip(*sentences))
    return sentences
