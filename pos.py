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
    to_write = ''
    for word in tagged:
    	to_write += str(word[0]) + '(' + str(word[1]) + ') '
    to_write += '\n'
    tagged_sentences.write(to_write)

dictionary = []
f = open(dictionary_file)
for line in f:
	dictionary.append(line)
f.close()

output = open('output_dictionary.txt', 'w')

for line in dictionary:
	words = nltk.word_tokenize(line)
	tagged = nltk.pos_tag(words)
	
	to_write = ''
	to_write += str(tagged[0][0])
	to_write += str(tagged[1][0])
	for i in range(2, len(tagged)):
		if tagged[i][0] != ',':
			to_write += str(tagged[i][0]) + '/' + str(tagged[i][1])
		else:
			to_write += str(tagged[i][0]) + ' '
	to_write += '\n'

	output.write(str(to_write))


tagged_sentences.close()
output.close()