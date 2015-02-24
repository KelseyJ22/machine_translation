import math, collections

# A stupid backoff language model for choosing the most fluent/likely sentence from possible translations
class NaiveBayesSBLM:

  def __init__(self, corpus):
    self.unigramCounts = collections.defaultdict(lambda: 1)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    for sentence in corpus.corpus:
        prev = "<s>"
        for datum in sentence.data:  
            token = datum.word
            self.unigramCounts[token] = self.unigramCounts[token] + 1
            bigram_token = prev + "|" + token
            self.bigramCounts[bigram_token] = self.bigramCounts[bigram_token] + 1
            prev = token
            self.total += 1

  def score(self, sentence):
    score = 0.0
    prev = "<s>"
    V = len(self.unigramCounts.keys())
    for token in sentence:
        bigram_token = prev + "|" + token
        count = self.bigramCounts[bigram_token]
        if count <= 0: #backoff
            count = self.unigramCounts[token]
            score += math.log(count)
            score -= math.log(0.4*(self.total + V))
        else:
            score += math.log(count)
            score -= math.log(self.unigramCounts[prev])
        prev = token

    return score
