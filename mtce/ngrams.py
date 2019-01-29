
from collections import Counter, defaultdict

MAX_N = 4

def get_ngrams(sent, n):
    ngs = [ ng for ng in zip(*(sent[i:] for i in range(n)))]
    return Counter(ngs)

def get_confirmed(refgrams, Agrams):
    conf = Counter()
    for gr,c in Agrams.items():
        conf.update({gr:min(refgrams[gr],c)})
    return conf

def get_unconfirmed(refgrams, Agrams):
    return get_confirmed(Agrams, refgrams)

def get_firmed_ngrams(reference, A, B, n, get_firmed):
    """
    gets the data to show confirmed and unconfirmed n-grams
    :param reference:
    :param A:
    :param B:
    :return:
    """
    Aconf = Counter()
    Bconf = Counter()
    for rl, Al, Bl in zip(reference,A,B):
        rg = get_ngrams(rl, n)
        Ag = get_ngrams(Al, n)
        c = get_firmed(rg,Ag)
#        print(rl)
#        print(Al)
#        print(c)
        Aconf.update(c)
        Bg = get_ngrams(Bl,n)
        Bconf.update(get_firmed(rg,Bg))

    all_firmed = []
    for ng in set(Bconf.keys()).union(Aconf.keys()):
        a = Aconf[ng]
        b = Bconf[ng]
        ng = " ".join(ng)
        all_firmed.append((ng,a,b,a-b))
    all_firmed = sorted(all_firmed, key=lambda t:t[3], reverse=True)
    return all_firmed

def get_all_confirmed_ngrams(reference, A, B, beg, end):
    return [(n,get_firmed_ngrams(reference, A, B, n, get_confirmed)[beg:end]) for n in range(1,MAX_N+1)]

def get_all_unconfirmed_ngrams(reference, A, B, beg, end):
    return [(n,get_firmed_ngrams(reference, A, B, n, get_unconfirmed)[beg:end]) for n in range(1,MAX_N+1)]
