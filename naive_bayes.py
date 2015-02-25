import math, collections

# A stupid backoff language model for choosing the most fluent/likely sentence from possible translations
class NaiveBayesSBLM:

  def __init__(self, corpus):
    self.unigramCounts = collections.defaultdict(lambda: 1)
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  # PARAMS:
  # @corpus => list of sentences (lists)
  # VARS:
  # @sentence => list of words (strs)
  # @word => strs
  def train(self, corpus):
    for sentence in corpus:
        prev = "<s>"
        for word in sentence:  
            self.unigramCounts[word] = self.unigramCounts[word] + 1
            bigram_token = prev + "|" + word
            self.bigramCounts[bigram_token] = self.bigramCounts[bigram_token] + 1
            prev = word
            self.total += 1

  def score(self, sentence):
    score = 0.0
    prev = "<s>"
    V = len(self.unigramCounts.keys())
    for word in sentence:
        bigram_token = prev + "|" + word
        count = self.bigramCounts[bigram_token]
        if count <= 0: #backoff
            count = self.unigramCounts[word]
            score += math.log(count)
            score -= math.log(0.4*(self.total + V))
        else:
            score += math.log(count)
            score -= math.log(self.unigramCounts[prev])
        prev = word

    return score
