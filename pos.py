#!/usr/bin/env python

from nltk.corpus import cess_esp
import nltk

#For English post-processing, the path will need to be replaced with an
#initialization of the English sentences list
sentences_file = 'data/sentences.txt'

contents = []
f = open(sentences_file)
for line in f:
    contents.append(line)
f.close()


spanish_training = cess_esp.tagged_sents()
##TODO
#For English post-processing the line below should be commented out
tagger = nltk.UnigramTagger(spanish_training)

for line in contents:
    words = nltk.word_tokenize(line)

    #For english post-processing, the line below will need to be commented out
    #and replaced with the line below it
    print(tagger.tag(words))
    #print(nltk.pos_tag(words))
