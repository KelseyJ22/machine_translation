#!/usr/bin/env python

from nltk.corpus import cess_esp
import nltk

#For English post-processing, the path will need to be replaced with an
#initialization of the English sentences list
sentences_file = 'data/sentences.txt'
dictionary_file = 'data/dictionary.txt'

contents = []
f = open(sentences_file)
for line in f:
    contents.append(line)
f.close()

tagged_sentences = open('tagged_sentences.txt', 'w')

spanish_training = cess_esp.tagged_sents()
tagger = nltk.UnigramTagger(spanish_training)

for line in contents:
    words = nltk.word_tokenize(line)
    tagged = tagger.tag(words)
    tagged_sentences.write(str(tagged))

dictionary = []
f = open(dictionary_file)
for line in f:
	dictionary.append(line)
f.close()

output = open('output_dictionary.txt', 'w')

for line in dictionary:
	words = nltk.word_tokenize(line)
	tagged = nltk.pos_tag(words)
	output.write(str(tagged))


tagged_sentences.close()
output.close()