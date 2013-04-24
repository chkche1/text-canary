import dictionary_reader as dr
import numpy
import operator
from collections import defaultdict

class Analyzer:
    pos_cnt = defaultdict(int)
    neg_cnt = defaultdict(int)

    def __init__(self):
        self.big = dr.BigDictionary()
        self.affect = dr.AffectDictionary()

    def count_cue(self, text, pos, tbl=dr.twitter2mpqa_tbl):
        """
        input:
        tweet is the preprocessed tweet text
        posi is the pos tag for each token
        output:
        sentiment: (num_of_positive_cues, num_of_negative_cues)
        """
        posi, neg, tag = 0, 0, ''
        for idx, elem in enumerate(text):
            if pos[idx] not in tbl:
                tag = 'E' # assume it's emoticon
            else:
                tag = tbl[pos[idx]]
            sent = self.big.lookup(elem, tag)
            if sent<0:
                neg +=1
            elif sent==1:
                posi +=1
            elif sent >1:
                posi +=1
                neg +=1

        return (posi, neg)

    def get_emotion(self, text):
        """
        input:
        tweet is the preprocessed tweet text
        pos is the pos tag for each token
        output:
        joy, disgust, anger, fear, sadness, surprise, neutral
        """
        emo = defaultdict(int)
        for elem in text:
            t = self.affect.lookup(elem)
            emo[t[1]] += 1
        return emo

    def pmi(self, text):
        """
        Compute the average SO of the tweet
        """
        pmi = 0
        for token in text:
            pmi += numpy.log((0.01+Analyzer.pos_cnt[token])/(0.01+Analyzer.neg_cnt[token]))

        return pmi/len(text)

    def count(self, text, pos):
        """
        Count the cooccurence of each token in tweet and a sentiment cue. The
        result is stored in class variables. Make sure you run the function
        on all tweets before using the pmi function
        """
        for idx, elem in enumerate(text):
            nbr = self._near(text, idx)
            Analyzer.pos_cnt[elem] += len([x for x in nbr if
                    self.big.lookup(x,pos[idx])==1])
            Analyzer.neg_cnt[elem] += len ([x for x in nbr if
                    self.big.lookup(x,pos[idx])==-1])
            both = len([x for x in nbr if self.big.lookup(x, pos[idx])==2])
            Analyzer.pos_cnt[elem]+= both
            Analyzer.neg_cnt[elem]+= both

    def reset_cnt(self):
        pos_cnt, neg_cnt = defaultdict(int), defaultdict(int)

    def _near(self,a, tok_idx, n=10):
        """
        the NEAR operator: articles is a list of tokens
        """
        before = a[:tok_idx][-n:]
        after = a[tok_idx:][1:n+1]
        return before+after
