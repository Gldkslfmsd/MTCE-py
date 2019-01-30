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
        self.metrics_float_values = list(map(float,metrics_values))
        if metrics is None:
            metrics = []
        self.metrics = metrics
        self.has_metrics = metrics_values != []

    def add_metric_value(self, metric, value):
        self.metrics_float_values.append(value)
        value = "%2.2f" % value
        self.metrics_values.append(value)
        if metric not in self.metrics:
            self.metrics.append(metric)
        self.has_metrics = True

    def orderkey(self, metric):
        assert metric in self.metrics
        return self.metrics_float_values[self.metrics.index(metric)]




def get_translation_sentences(checkpoint, show):
    name = "%s:%s" % (checkpoint.mtsystem.name, checkpoint.name)
    sents = [ Sentence(checkpoint.id, name, text, show) for text in checkpoint.get_plain_sentences("translation") ]
    sent_ev_dict = checkpoint.get_sentence_evaluations_dict()
    for m in METRICS:
        if m not in sent_ev_dict: continue
        values = sent_ev_dict[m]
        for sent, v in zip(sents, values):
            sent.add_metric_value(m,v)
    return sents

def get_nontranslation_sentences(id,name, texts, show):
    return [Sentence(id, name, t, show) for t in texts ]

def get_metasentences(mf, id, show):
    return [Sentence(id, mf.name, t, show) for t in mf.get_sentences()]

def get_all_sentences(comp, system=None):
    # src and ref
    sentences = [get_nontranslation_sentences("src","source",comp.get_plain_sentences("source"),True)]
    for mf in comp.get_metafiles():
        if mf.owner_type == type_dict["source.txt"]:
            s = get_metasentences(mf, "meta-src", False)
            sentences.append(s)
    sentences.append(get_nontranslation_sentences("ref","reference",comp.get_plain_sentences("reference"),True))
    for mf in comp.get_metafiles():
        if mf.owner_type == type_dict["reference.txt"]:
            s = get_metasentences(mf, "meta-ref", False)
            sentences.append(s)

    if system is None:
        systems_checkpoints = comp.systems_checkpoints()
    else:
        systems_checkpoints = [ (s,ch) for s,ch in comp.systems_checkpoints() if s==system]

    # add the translation with metrics
    for i,(sys,cp) in enumerate(systems_checkpoints):
        s = get_translation_sentences(cp,i<2)
        sentences.append(s)
        for mf in cp.get_metafiles():
            s = get_nontranslation_sentences("meta-%s" % cp.id, mf.name, mf.get_sentences(), i<2)
            sentences.append(s)

    # Transpose. Now it has a shape [[src, ref, checkpoint1, checkpoint2...], [src, ref, ...]]
    sentences = list(zip(*sentences))
    return sentences




