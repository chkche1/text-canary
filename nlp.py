import nltk
import subprocess
import time
import spell_checker as spell
import os
import dictionary_reader as dr
import copy
import analyzer

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
analyzer = analyzer.Analyzer()
TWIT_TAGGER_PATH = './twit-tagger/runTagger.sh'

def twit_pos(text, batch=False):
    """ Performs POS tagging for Tweets
    """
    filename = str(time.time())+".pos"
    with open(filename,'w') as f:
        f.write(text)
    try:
        output = subprocess.Popen([TWIT_TAGGER_PATH, filename],\
                        stdout=subprocess.PIPE).communicate()[0]
    except:
        return None
    finally:
        os.remove(filename)
    elements = output.split('\t')
    return (elements[0].split(), elements[1].split())

def spellcheck(raw):
    """ Performs spell correction on the input
    """
    l = []
    sents = nltk.tokenize.sent_tokenize(raw)
    for sent in sents:
        words = nltk.word_tokenize(sent)
        for word in words:
            l.append(spell.correct(word))
    return ' '.join(l)

def postag(raw):
    """ Performs general POS tagging
    """
    ret = []
    sents =  nltk.tokenize.sent_tokenize(raw)
    for sent in sents:
        tokens = nltk.word_tokenize(raw)
        ret.extend(nltk.pos_tag(tokens))
    elems = zip(*ret)
    return (elems[0],elems[1])

def reduce_form(pairs):
    """ Lemmatize each token in input
    """
    ret = copy.deepcopy(pairs)
    for idx, (tok, pos) in enumerate(pairs):
        tag = pos
        if tag in dr.tag2lemmatizer:
            tag = dr.tag2lemmatizer[tag]
        else:
            continue
        ret[idx][0] = lemmatizer.lemmatize(tok,tag).lower()
    return ret

def preprocess(text, twit=False):
    """ Preprocess text for sentiment analysis
    """
    tagger = twit_pos if twit else postag
    toks, pos = tagger(text)
    tokens = [spell.correct(t) for t in toks]
    pairs = map(list, zip(tokens,pos))
    return reduce_form(pairs)

def emotion_analysis(raw, is_twit=False):
    pairs = preprocess(raw,twit=is_twit) if is_twit else preprocess(raw)
    toks, pos = zip(*pairs)
    return analyzer.get_emotion(toks)

def polarity_dist(raw, is_twit=False):
    pairs = preprocess(raw,twit=is_twit) if is_twit else preprocess(raw)
    toks, pos = zip(*pairs)
    tbl = dr.twitter2mpqa_tbl if is_twit else dr.postag2mpqa_tbl
    posi, neg = analyzer.count_cue(toks,pos,tbl)
    return {'positive':posi, 'negative':neg}

def get_avg_pmi(raw, is_twit=False):
    analyzer.reset_cnt()
    pairs = preprocess(raw,twit=id_twit) if is_twit else preprocess(raw)
    toks, pos = zip(*pairs)
    tbl = dr.twitter2mpqa_tbl if is_twit else dr.postag2mpqa_tbl
    analyzer.count(toks, pos)
    return analyzer.pmi(toks)
