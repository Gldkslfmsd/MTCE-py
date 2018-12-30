import numpy as np
from sacrebleu import *
import pickle

import datetime

def now():
    return datetime.datetime.now()

SEED = 1234
SAMPLE_SIZE = 100

# Masks are stored in a dict of following form:
# { line_number: (RandomState, [mask_for_sample_id_0, mask_for_sample_id_1, ...]), ... }
#  They are generated as requested.
masks_cache = {}

# TODO: this is not advisable in production... solve it later
with open("masks_cache.pickle","rb") as f:
    #print("opening masks", now())
    masks_cache = pickle.load(f)
    #print("done", now())

def get_mask(lines, sample_id, sample_size=None):
    assert sample_id >= 0
    if sample_size is None:
        sample_size = SAMPLE_SIZE
    assert sample_size >= 1

    if (lines,sample_size) in masks_cache:
        rs, masks = masks_cache[(lines,sample_size)]
    else:
        rs = np.random.RandomState(SEED)
        masks = []
        masks_cache[(lines,sample_size)] = (rs,masks)
    while sample_id+1 > len(masks):
        if sample_size > lines:
            replace = True
        else:
            replace = False
        m = rs.choice(lines,sample_size,replace=replace)
        masks.append(m)
    return masks[sample_id]

def get_masks(translation_file, count, sample_size=None):
    with open(translation_file,"r") as f:
        lines = sum(1 for _ in f)
    get_mask(lines, count, sample_size)
    return [ get_mask(lines, i, sample_size) for i in range(count) ]

def line_corpus_stats(sys_stream, ref_streams, lowercase=False, tokenize=DEFAULT_TOKENIZER):
    """Produces BLEU scores along with its sufficient statistics from a source against one or more references.

    :param sys_stream: The system stream (a sequence of segments)
    :param ref_streams: A list of one or more reference streams (each a sequence of segments)
    :param smooth: The smoothing method to use
    :param smooth_floor: For 'floor' smoothing, the floor to use
    :param force: Ignore data that looks already tokenized
    :param lowercase: Lowercase the data
    :param tokenize: The tokenizer to use
    :return: a BLEU object containing everything you'd want
    """

    # Add some robustness to the input arguments
    if isinstance(sys_stream, str):
        sys_stream = [sys_stream]
    if isinstance(ref_streams, str):
        ref_streams = [[ref_streams]]

#    sys_len = 0
#    ref_len = 0

#    _correct = [0 for n in range(NGRAM_ORDER)]
#    _total = [0 for n in range(NGRAM_ORDER)]

    # look for already-tokenized sentences
#    tokenized_count = 0

    line_stats = []

    fhs = [sys_stream] + ref_streams
    for lines in zip_longest(*fhs):
        if None in lines:
            raise EOFError("Source and reference streams have different lengths!")

        if lowercase:
            lines = [x.lower() for x in lines]

#        if not (force or tokenize == 'none') and lines[0].rstrip().endswith(' .'):
#            tokenized_count += 1
#
#            if tokenized_count == 100:
#                logging.warning('That\'s 100 lines that end in a tokenized period (\'.\')')
#                logging.warning('It looks like you forgot to detokenize your test data, which may hurt your score.')
#                logging.warning('If you insist your data is detokenized, or don\'t care, you can suppress this message with \'--force\'.')

        output, *refs = [TOKENIZERS[tokenize](x.rstrip()) for x in lines]
        ref_ngrams, closest_diff, closest_len = ref_stats(output, refs)

#        sys_len += len(output.split())
#        ref_len += closest_len

        lstat = [len(output.split()), closest_len]

        correct = [0 for n in range(NGRAM_ORDER)]
        total = [0 for n in range(NGRAM_ORDER)]

        sys_ngrams = extract_ngrams(output)
        for ngram in sys_ngrams.keys():
            n = len(ngram.split())
            correct[n-1] += min(sys_ngrams[ngram], ref_ngrams.get(ngram, 0))
#            _correct[n-1] += min(sys_ngrams[ngram], ref_ngrams.get(ngram, 0))
            total[n-1] += sys_ngrams[ngram]
#            _total[n-1] += sys_ngrams[ngram]
        lstat += correct + total
        line_stats.append(np.array(lstat))

#    a = np.array(line_stats)
#    print(np.sum(a, axis=0))
#    print(np.array([sys_len, ref_len]+_correct+_total))
    return np.array(line_stats)
#    return compute_bleu(correct, total, sys_len, ref_len, smooth, smooth_floor, use_effective_order)


def bootstrap_corpus_bleu(sys_stream, refs, masks,
                         smooth='exp', smooth_floor=0.0, force=False, lowercase=False,
                          tokenize=DEFAULT_TOKENIZER, use_effective_order=False):

    sample_bleus = []
    line_stats = line_corpus_stats(sys_stream, refs, lowercase=lowercase, tokenize=tokenize)
    for mask in masks:
        stats = np.sum(line_stats[mask],axis=0)
        sys_len, ref_len, *_ = stats
        correct = stats[2:2+NGRAM_ORDER]
        total = stats[2+NGRAM_ORDER:]

        bl = compute_bleu(correct, total, sys_len, ref_len, smooth, smooth_floor, use_effective_order)
        sample_bleus.append(bl.score)

    return sample_bleus

